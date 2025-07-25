# Copyright (C) 2023 Rastislav Kish
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from os import path

import base64
import click
import requests

class SystemMessage:

    def __init__(self, text):
        self._text=text

    def text(self):
        return self._text

    def render(self):
        return {
            "role": "system",
            "content": [
                {"type": "text", "text": self._text}
                ],
            }
class Message:

    def __init__(self, text):
        self._text=text

    def text(self):
        return self._text

    def render(self):
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": self._text}
                ],
            }
class ImageMessage:

    def __init__(self, text, images):
        self._text=text
        self._images=images

    def text(self):
        return self._text

    def render(self):
        content=[{
            "type": "text",
            "text": self._text,
            }]
        content+=[image.render() for image in self._images]

        result={
            "role": "user",
            "content": content,
            }

        return result
class GptResponse:

    def __init__(self, text):
        self._text=text

    def text(self):
        return self._text

    def render(self):
        return {
            "role": "assistant",
            "content": [
                {"type": "text", "text": self._text}
                ],
            }

class Image:

    def from_input(input):
        if path.exists(input) and path.isfile(input):
            with open(input, "rb") as f:
                image=f.read()
                image=base64.b64encode(image).decode("utf-8")
                return LocalImage(image)
        if input.startswith("http"):
            return RemoteImage(input)
class LocalImage(Image):

    def __init__(self, image):
        super().__init__()
        self._image=image

    def render(self):
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{self._image}",
                },
            }
class RemoteImage:

    def __init__(self, url):
        super().__init__()
        self._url=url

    def render(self):
        return {
            "type": "image_url",
            "image_url": {
                "url": self._url,
                },
            }

class Conversation:

    def __init__(self, api_key, model, system_message):
        self._api_key=api_key
        self._model=model
        self._messages=[]

        if system_message:
            self._messages.append(system_message)

        self._total_used_input_tokens=0
        self._total_used_output_tokens=0

    def push_message(self, message):
        self._messages.append(message)
    def generate_response(self):
        messages=[message.render() for message in self._messages]

        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}"
            }
        body={
            "model": self._model,
            "messages": messages,
            "max_tokens": 300
            }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
        res=response.json()

        if "error" in res:
            return f"Error: {res['error']['message']}"

        if "usage" in res:
            self._total_used_input_tokens+=res["usage"]["prompt_tokens"]
            self._total_used_output_tokens+=res["usage"]["completion_tokens"]

        if "choices" in res:
            if "content" in res["choices"][0]["message"]:
                message=GptResponse(res["choices"][0]["message"]["content"])
                self.push_message(message)

                return message.text()

        return None

    def total_price(self):
        return 0.0025*(self._total_used_input_tokens/1000)+0.01*(self._total_used_output_tokens/1000)

@click.command()
@click.option("-a", "--api-key", envvar="OPENAI_API_KEY", help="The OpenAI api key")
@click.option("-s", "--system-prompt", default="", help="The system prompt to use")
@click.option("-u", "--user-prompt", default="What's in the image?", help="The first user prompt to use if images are passed")
@click.argument("images", nargs=-1)
def main(api_key, system_prompt, user_prompt, images):
    """A simple program that opens a conversation about image with GPT 4o"""

    loaded_images=[]
    for inp in images:
        image=Image.from_input(inp)

        if image==None:
            print(f"Error: Unable to process {input}")
            return

        loaded_images.append(image)
    images=loaded_images

    conversation=Conversation(api_key, "gpt-4o", SystemMessage(system_prompt) if system_prompt!="" else None)

    if len(images)>0:
        message=ImageMessage(user_prompt, images)
        conversation.push_message(message)
        response=conversation.generate_response()
        print(response)

    while True:
        try:
            inp=input("Enter your message")
        except EOFError:
            break

        if inp=="":
            continue

        message=Message(inp)
        conversation.push_message(message)
        response=conversation.generate_response()
        print(response)

    print(f"Conversation price: {conversation.total_price()}")

if __name__=="__main__":
		main()
