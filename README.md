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

`city <city>` - Prints out current location, changes location if `<city>` is provided

`changeloc` - Starts the location-changing flow (same effect as `city <city>`, but in a more interactive manner)

`exit` - Actually exits the program

Controlled device(s):
---
- [Cololight Strip](https://cololight.de/products/cololight-strip?variant=32881788387392) (props to [pycololight](https://github.com/BazaJayGee66/pycololight) for reverse-engineering their API)

Usage:
---
### Windows:
- Pull the repo (don't forget to change working directory)
- Run `make setup` if running for the first time, otherwise `make run` will suffice
- Profit!

### Unix-like:
- Coming soon!
