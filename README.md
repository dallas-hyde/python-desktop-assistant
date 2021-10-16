# python-desktop-assistant
 
## What is this?
This is a personal desktop assistant written in Python and Tkinter.

## How does it work?
1. Download the repo and copy the default configuration files that end in `.json`.
2. Rename the copied files to `clock.json` and `weather.json`.
3. You can then edit the configuration of the clock and weather widgets through their configuration files.
4. You should get an [OpenWeatherMap](https://openweathermap.org/) account setup and put your API key, zip code and country abbreviation in the corresponding fields inside of your `weather.json`.
5. You then install the required pip packages using the `requirements.txt` file.
6. Then you run `python ./src/main.py`.

You can close the application by right clicking on any of the text and the window bar will appear, you can then close the application.
NOTE: This can sometimes be a bit finicky, just keep trying or you can kill the program from your process list.

## LINUX / MAC IMPORTANT
**Linux:**
Linux tkinter does not support completely transparent backgrounds so the app will have a semi transparent grey background.
Linux also has issues displaying emoji, so in the `weatherTypes` field inside of `weather.json` you can put text or other symbols to represent the weather types.

**Mac:**
I can't test Mac compatability because I don't own a Mac.

If there are any issues on Mac, feel free to let me know and I'll try my best to fix them.
