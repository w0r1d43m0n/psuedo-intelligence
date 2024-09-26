from tkinter import *
from tkinter.ttk import *

class responseNotification():
	def __init__(self, response):
		self.window = Tk()

		width = self.window.winfo_screenwidth()
		height = self.window.winfo_screenheight()

		self.window.title("Response from API")
		self.window.geometry(f"{round(width * 0.15)}x{round(height * 0.8)}+{round(width * 0.05)}+{round(height * 0.05)}")

		self.html = Label(self.window, text=response)
		self.html.bind('<Configure>', lambda e: self.html.config(wraplength=self.html.winfo_width()))
		self.html.pack()

		self.window.mainloop()

