# GrowCastleBot
## Setup
In order for this bot to work you need to do a few steps with adb and scrcpy:
1. Plug your phone to your computer
2. run the command: `adb tcpip <port>`
3. Unplug your phone from your computer
4. run the command: `adb connect <phone_ip>:<port>`
5. run scrcpy
## Installation
Just run `pip install -r requirements.txt`
## Running
>
>usage: play_growcastle.py [-h] [--scrcpy_window_name SCRCPY_WINDOW_NAME] {replay,battle}
>
>This script will automate level advancements for grow castle
>
>positional arguments:
>  {replay,battle}       Whether to replay the same level or battle
>
>optional arguments:
>  -h, --help            show this help message and exit
>  --scrcpy_window_name SCRCPY_WINDOW_NAME, -w SCRCPY_WINDOW_NAME
>                        The name of the window of scrcpy. This is for optimizations