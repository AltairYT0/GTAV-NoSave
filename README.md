# GTAV-NoSave

## Description
This program implements firewall rules to prevent communication with Rockstar servers. The original concept comes from [this Reddit post](https://www.reddit.com/r/gtaglitches/comments/okz5lg/exploit_pc_v1_nosavingsaveblock_method_ahk_replay/). For a comprehensive understanding of the method, please read the original post thoroughly.

This project is simply a enhanced UI implementation of the original concept, offering a more user-friendly interface while maintaining the same core functionality.

## Requirements
- Python 3.x
- Required libraries:
  - pip install keyboard tk
 

## Usage
1. Ensure GTA V is running in windowed or borderless mode (not fullscreen)
2. Launch GTA Online and wait until you have full control of your character
3. Run `GTAV-NoSave.py`
4. Use the following keybinds:
 - Enable: `Ctrl + F9`
 - Disable: `Ctrl + F12`
5. After finishing, run `cleaner.py` to remove the created firewall rules
6. Key bindings may occasionally become non-functional due to Rockstar's preventive measures. To ensure proper operation of the program, you should launch it and press 'Ctrl + F9' approximately 20 seconds before completing the mission. Upon successful activation, a notification window displaying 'Enabled' should appear on the right side of your screen.

## Important Notes
- This is built using Python with keyboard, tkinter, and datetime libraries
- Always run `cleaner.py` after usage to ensure proper cleanup
- Program must be run with administrative privileges

## Disclaimer
⚠️ USE AT YOUR OWN RISK! I take no responsibility for any damages that may occur to your computer or game account. This tool is provided as-is, and usage is at the user's discretion and responsibility.
