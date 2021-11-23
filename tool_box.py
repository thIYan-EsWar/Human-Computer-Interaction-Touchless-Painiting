import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox as alert

import yaml

CHOOSE_COLOR = False

def destroy_window(window: tk.Tk):
	global CHOOSE_COLOR
	CHOOSE_COLOR = not CHOOSE_COLOR
	window.destroy()

def color_palette():
	window = tk.Tk()

	display = tk.Entry(window, borderwidth=5)
	display.grid(row=0, column=0, columnspan=2, ipadx=10, ipady=10)

	def destroy():
		if alert.askokcancel('Exit', 'Do you really want to quit?'):
			CHOOSE_COLOR = False
			window.destroy()

	def color_palette():
		display.delete(0, tk.END)
		color, _ = colorchooser.askcolor()
		color = (0, 0, 0) if not color else color
		with open('tools.yaml', 'w') as f:
			yaml.dump({'color': color}, f)
		display.insert(0, color)

	tk.Button(window, text='Choose', command=color_palette).grid(row=1, column=0)
	tk.Button(window, text='Close ',command=window.destroy).grid(row=1, column=1)

	window.protocol('WM_DELETE_WINDOW', destroy)

	window.mainloop()