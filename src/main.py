# Windowing
import tkinter
import tkinter.ttk
import time


# Weather
import pyowm
import pyowm.utils.config
import pyowm.utils.timestamps
import pyowm.weatherapi25.observation
import pyowm.weatherapi25.weather
import pyowm.weatherapi25.weather_manager


# Json
import json


class ClockWidget(tkinter.Frame):
	def __init__(self, parent: tkinter.Tk, settings: dict) -> None:
		super().__init__(parent)

		self.configure(background="grey")

		# Save the settings and declare the clock variables
		self.settings: dict = settings
		self.time_as_string: str = ""
		self.time_suffix: str = ""

		# Create the label
		self.label: tkinter.Label = tkinter.Label(self, font=("digital numbers", 36), background="grey", foreground="white")
		self.label.pack(anchor="center")


	def update_widget(self) -> None:
		print("Updating Clock!")
		# Get the correct time and time suffix based on user settings
		if self.settings.get("timeFormat") == 12:
			self.time_as_string = time.strftime("%I:%M")

			if not self.time_suffix:
				self.time_suffix = time.strftime(" %p")
		
		else:
			self.time_as_string = time.strftime("%H:%M")

			if self.time_suffix:
				self.time_suffix = ""
		
		# If the user has configured to show seconds then append the seconds
		if self.settings.get("showSeconds"):
			self.time_as_string = str(self.time_as_string, ":", time.strftime("%S"))
		
		# Update the text of the label
		self.label.configure(text="{0}{1}".format(self.time_as_string, self.time_suffix))
		# Schedule the next update
		self.after(self.settings.get("updateTimeInMillis"), self.update_widget)


class WeatherWidget(tkinter.Frame):
	def __init__(self, parent: tkinter.Tk, settings: dict) -> None:
		super().__init__(parent)

		self.configure(background="grey")

		# Save the settings and declare weather variables
		self.settings = settings
		self.weather_map: pyowm.OWM = pyowm.OWM(settings.get("apiKey"))
		self.weather_manager: pyowm.weatherapi25.weather_manager.WeatherManager = self.weather_map.weather_manager()
		self.observation: pyowm.weatherapi25.observation.Observation
		self.weather: pyowm.weatherapi25.weather.Weather

		# Create the labels
		self.weather_label: tkinter.Label = tkinter.Label(self, font=("digital numbers", 36), background="grey", foreground="white")
		self.weather_label.pack(anchor="center")
		self.temperate_label: tkinter.Label = tkinter.Label(self, font=("digital numbers", 36), background="grey", foreground="white")
		self.temperate_label.pack(anchor="center")


	def update_widget(self) -> None:
		print("Updating Weather!")
		# Get the current weather
		self.observation = self.weather_manager.weather_at_zip_code(self.settings.get("zipCode"), self.settings.get("country"))
		self.weather = self.observation.weather

		# Update the text of the labels
		self.weather_label.configure(text=str(self.settings.get("weatherTypes").get(str(self.weather.status).lower())))
		self.temperate_label.configure(text="{0}°{1}".format(int(self.weather.temperature(self.settings.get("temperatureUnits").lower()).get("temp")), self.settings.get("temperatureUnits")[0].upper()))
		# Schedule the next update
		self.after(self.settings.get("updateTimeInMillis"), self.update_widget)


class DesktopAssistant(tkinter.Tk):
	def __init__(self, clock_settings: dict, weather_settings: dict) -> None:
		super().__init__()

		# Configure the window
		self.title("Python-Desktop-Assistant")
		self.configure(background="grey")
		# Prevent the window from being resized
		self.resizable(0, 0)
		self.hide_window: bool = True
		# Make the window non-closable
		self.overrideredirect(self.hide_window)
		# Set the background of the window to transparent
		self.wm_attributes("-transparentcolor", "grey")
		# Ensuer the label will be on top of windows
		self.wm_attributes("-topmost", True)
		# Make the window transparent
		self.wm_attributes("-alpha", 0.5)
		# Bring the window to the front
		self.lift()

		# Bind the window's events to functions
		self.bind("<Button-3>", self.on_right_click)
		self.bind("<Enter>", self.on_enter)
		self.bind("<Leave>", self.on_leave)

		# Create the clock widget
		self.clock: ClockWidget = ClockWidget(self, clock_settings)
		self.clock.pack(anchor="center")

		# Attempt to create the weather widget if the settings exist and it contains an API key
		if weather_settings and weather_settings.get("apiKey"):
			self.weather: WeatherWidget = WeatherWidget(self, weather_settings)
			self.weather.pack(anchor="center")

		# Update the created widgets
		self.clock.update_widget()
		# NOTE: A more scalable solution would be to append the widgets to an array and then update them all at once
		if self.weather:
			self.weather.update_widget()


	def on_enter(self, event: tkinter.Event) -> None:
		# Make the window opaque when moused over
		self.wm_attributes("-alpha", 1.0)


	def on_leave(self, event: tkinter.Event) -> None:
		# Make the window transparent when not moused over
		self.wm_attributes("-alpha", 0.5)


	def on_right_click(self, event: tkinter.Event) -> None:
		self.hide_window = not self.hide_window
		self.overrideredirect(self.hide_window)


if __name__ == '__main__':
	clock_settings: dict = {}
	weather_settings: dict = {}

	# Load clock settings
	try:
		with open("./clock.json", "r") as file:
			clock_settings = json.load(file)
	
	except FileNotFoundError:
		try:
			with open("./default_clock.json", "r") as file:
				clock_settings = json.load(file)
		
		except FileNotFoundError:
			print("Default Clock Configuration File Not Found!")
	
	# Load weather settings
	try:
		with open("./weather.json", "r") as file:
			weather_settings = json.load(file)
	
	except FileNotFoundError:
		try:
			with open("./default_weather.json", "r") as file:
				weather_settings = json.load(file)
		
		except FileNotFoundError:
			print("Default Weather Configuration File Not Found!")
	
	if clock_settings:
		desktop_assistant: DesktopAssistant = DesktopAssistant(clock_settings, weather_settings)
		desktop_assistant.mainloop()
