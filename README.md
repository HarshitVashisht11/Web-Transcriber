# Web Transcriber

Web Transcriber is a web-based application that allows users to transcribe audio and video files using OpenAI's Whisper ASR model. The application provides a user-friendly interface for uploading files, selecting language and model options, and generating transcriptions.

## Features

- Transcribe audio and video files to text.
- Choose from different language and model options.
- User-friendly web interface.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/HarshitVashisht11/Web-Transcriber.git

2. Install Flask:

   ```
   pip install flask

3. Install PyTorch:

   ```
   pip install torch

5. Install Whisper:
   ```
    pip install -U openai-whisper
   
6. it also requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers:
    ```
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg

    # on Arch Linux
    sudo pacman -S ffmpeg

    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg

    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg

    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg

# Using GPU
The Web Transcriber supports GPU acceleration for faster transcription. Ensure that you have a compatible GPU and the necessary GPU drivers installed. The application uses the GPU to enhance the speed of the transcription process.

There are five model sizes, four with English-only versions, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model; actual speed may vary depending on many factors including the available hardware.

|  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

