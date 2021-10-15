import tkinter
import tkinter.ttk
import time


class DesktopAssistant(tkinter.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title("Python-Desktop-Assistant")

		self.hide_window: bool = True

		# Create the clock label
		self.clock_label = tkinter.Label(self, font=("digital numbers", 36), background="grey", foreground="white")
		self.clock_label.pack(anchor="center")

		# Make the window non-closeable
		self.clock_label.master.overrideredirect(self.hide_window)

		# Shift the label to the bottom left of the screen
		self.clock_label.master.geometry("+10+930")
		# Set the background of the clock label to transparent
		self.clock_label.master.wm_attributes("-transparentcolor", "grey")
		# Ensure the label will be on top of windows
		self.clock_label.master.wm_attributes("-topmost", True)

		# Make the window transparent
		self.clock_label.master.wm_attributes("-alpha", 0.5)

		# Bind the clock's events to functions
		self.clock_label.bind("<Button-3>", self.clock_right_click)
		self.clock_label.bind("<Enter>", self.clock_on_enter)
		self.clock_label.bind("<Leave>", self.clock_on_leave)

		# Bring the label to the front
		self.clock_label.master.lift()
	

	def update_clock(self) -> None:
		time_as_string: str = time.strftime("%I:%M:%S %p")
		self.clock_label.configure(text=time_as_string)
		self.clock_label.after(1000, self.update_clock)
	

	def clock_right_click(self, event: tkinter.Event) -> None:
		self.hide_window = not self.hide_window
		self.clock_label.master.overrideredirect(self.hide_window)
	

	def clock_on_enter(self, event: tkinter.Event) -> None:
		# Make the window transparent when not in focus
		self.clock_label.master.wm_attributes("-alpha", 1.0)
	

	def clock_on_leave(self, event:tkinter.Event) -> None:
		# Make the window transparent when not in focus
		self.clock_label.master.wm_attributes("-alpha", 0.5)


if __name__ == '__main__':
	desktop_assistant: DesktopAssistant = DesktopAssistant()
	desktop_assistant.update_clock()
	desktop_assistant.mainloop()
