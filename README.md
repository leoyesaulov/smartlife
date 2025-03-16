# Smartlife
This project's goal is to automatisate my smarthome appliances.

Current functionality:
---
- Turns the lights on/off depending on sun position (turn on right before sunset) and time (turn off after 23:00 local time)
- Lets turn the lights on/off manually
- Tries to turn lights off every 30 minutes after 23:00 local time (this activity can be paused with `timer`)

Available inputs:
---
`on <brightness=25> <time=0>` - Turns the lights on with `brightness` and starts the `timer` of `time` minutes.

`off <time=0>` - Turns the lights off and starts the `timer` of `time` minutes.

`timer <time>` - Sets the timer for `time` minutes (disables the automatic turning on/off for the duration of the timer)

`stop` - Kills all timers

Controlled device(s):
---
- [Cololight Strip](https://cololight.de/products/cololight-strip?variant=32881788387392) (props to [pycololight](https://github.com/BazaJayGee66/pycololight) for reverse-engineering their API)

Usage (makefile coming soon):
---
### Windows:
- Pull the repo
- Create `.env` in your root directory
- Place your strip's IP in `.env` as follows: `STRIP_IP="your_ip"`
- Create a new virtual environment inside of the project's folder with: `python -m venv .venv`
- Activate the virtual environment:
  -  For `cmd.exe` shell: `C:\> <path-to-.venv>\Scripts\activate.bat`
  -  For `Powershell`: `C:\> <path-to-.venv>\Scripts\Activate.ps1`
- Install the requirements by running: `pip install -r requirements.txt`
- run `main.py` with `python main.py`
- Profit!

### Unix-like:
- Coming soon!
