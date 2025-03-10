# smartlife
This project's goal is to automatisate my smarthome appliances.

Current functionality:
- Checks every 10 minutes if one of below actions needed:
- Turn the lights on/off depending on sun position (turn on right before sunset) and time (turn off after 23:00)
- Turn the lights on/off manually
- Try to turn lights off every 30 minutes after 23:00 (this activity can be paused with "timer x" command, where x = minutes)

Available inputs:
- on: turns on the lights with 25 brightness
- on x: turns on the lights with x brightness
- on x y: turns on the lights with x brightness and sets the timer for y minutes
- off: turns off the lights
- off x: turns off the lights and sets timer for x minutes
- timer x: sets the timer for x minutes (disables the automated turn on/off for the duration of the timer)
- stop: kills all timers
- anything else: prints "I'm sorry, I didn't understand that."

Controlled devices:
- Cololight Strip (thx to pycololight for reverse-engineering the api for these strips)

Usage (makefile soon):
- Pull the repo
- Create .env in root directory
- Place your strip's IP in .env in form of: STRIP_IP="your_ip"
- Create and enter venv
- Install requirements (run command "pip install -r requirements.txt")
- run main.py
- Profit!
