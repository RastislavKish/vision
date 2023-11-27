# Vision

This is a very simple script I wrote to make use of the new GPT 4 vision API and the amazing possibilities it brings. Note it's a very dynamic program I'm writing primarily for my own use, mostly because this is a new field the potential of which yet has to be discovered. Therefore it's not particularly polished and things can (and likely will) change during its development. I'm sharing the code in case anyone else finds it useful. And also because I need to version it anyway.

## Usage

A full-fledged prompt:

```
vision -s "You're a professor of biology on the Harward university." -u "What species of animals are visible on these images and what are their distinctive characteristics?" image1.jpg image2.jpg
```

Though most of the time, you can simply go with:

```
vision image.jpg
```

URLs are also supported:

```
vision https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/121px-Python-logo-notext.svg.png
```

Note only jpg, png, gif and webp formats are supported, leaving out svg, which is also very common. You may want to check the url's extension (if it's present) before sending.

"What's in the image?" is used as the default user prompt, which should fit the most general use-case of getting the description of a selected image.

After the image/s are described, you can interactively ask follow up questions about details and whatever you can think of, or simply use the program like you would interact with GPT 4 (GPT 4V is actually a full-fledged version of GPT 4, thus you can expect the same level of skills and capabilities).

You don'ŧ need to pass images at all, in that case, you will get a standard chat session.

Note discussion cropping is not implemented yet, so when interacting, you can only go as far as the token window of the model. Unless you include large materials or create a very long thread, you should be good asking quite a few questions for an image.

You can end the conversation by closing the pipe in your terminal (Ctrl+D on Linux). The program will show you the estimated price of your conversation according to OpenAI pricing at the time of writing the script. As a very rough approximation, recognition of a high-fidelity image costs around $0.01, which also needs to be charged with every follow-up question since the API doesn't maintain a state and therefore the whole conversation (including the images) needs to be resent to the server and re-evaluated. In other words, recognizing an image and asking 10 follow-up questions will cost approximately $0.1. If the costs are a matter, you may consider adjusting the user prompt to give you the seeked information as soon as possible and as shortly as possible, decreasing the token usage and the need for follow-up questions.

Also note these prices are approximations and can change in the future. Make sure to see the OpenAI [pricing](https://openai.com/pricing) for uptodate and accurate information. fo

## Setup

### Dependencies

The script is crossplatform, it needs Python to run, dependencywise, it requires click and requests Python packages. Run

```
pip3 install click requests
```

on Linux or:
```
pip install click requests
```

On Windows. Note you may need to create a virtual environment in some of the newer Linux distributions as packaged Python environments are getting preferred and the project doesn't have a package yet, this should be addressed soon. Or, alternatively, you can make use of your distribution-packaged Python libraries, which are less flexible but easier to setup:

```
sudo apt install python3-click python3-requests
```

### Get the OpenAI api key

Visit [platform.openai.com](https://platform.openai.com) to optain the API key for accessing OpenAI models. You can sign up using your ChatGPT account if you already have one, you need to add a billing method (using your debet card), load credit into your account and generate the API key.

You can either create OPENAI_API_KEY environment variable in your system to provide the key to vision, or pass it directly to the program through a flag (though this approach is not recommended).

### Running

On Linux, you can add execute permissions if necessary:

```
chmod +x vision
```

And run like any program:

```
./vision
```

On Windows, you can run the program using python:

```
python vision
```

## License

Copyright (C) 2023 Rastislav Kish

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

