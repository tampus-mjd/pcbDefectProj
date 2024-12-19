import os
import time
import threading
import ctypes

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, Menu

from PIL import Image, ImageTk

# variables
isCameraOn = False

# Create and initialize the main application window
root = Tk()

scrWidth = (root.winfo_screenwidth() // 1.5)
scrHeight = (root.winfo_screenheight() // 1.5)

# img = tk.PhotoImage(file="res/pcbDefect.png")
root.geometry("%dx%d+%d+%d" % (scrWidth, scrHeight, (scrWidth // 4), (scrHeight // 4)))
root.resizable(False, False)
root.title("pcbDefectProj")
# root.iconphoto(False, img)

# Menubar
menubar = tk.Menu(root)

menu_file = Menu(menubar, tearoff=0)
menu_file.add_command(label="Close", command=root.quit)

menu_camerasource = tk.Menu(menubar, tearoff=0)
menu_camerasource.add_radiobutton(label="source1", command='')
menu_camerasource.add_radiobutton(label="source2", command='')
menu_camerasource.add_separator()
menu_camerasource.add_command(label="camera_disable", command='')


menu_help = tk.Menu(menubar, tearoff=0)
menu_help.add_command(label="About...", command='')

menubar.add_cascade(label="File", menu=menu_file)
menubar.add_cascade(label="Camera Source", menu=menu_camerasource)
menubar.add_cascade(label="Help", menu=menu_help)

root.config(menu=menubar)


# Canvas
cameraFeed = tk.Canvas(root, borderwidth=2, relief="solid", bg="gray", height=(scrHeight - 20), width=(scrWidth - 20))
cameraFeed.place(x=5, y=5)


# Camera Feed Placeholder
placeholder_camOn = ImageTk.PhotoImage(Image.open("res/camOn.png"))
placeholder_camOff = ImageTk.PhotoImage(Image.open("res/camOff.png"))

# adding image to feed
# display_feed(isCameraOn)


"""
# Toggle button
btnCameraToggle = ttk.Button(root, text="Turn Camera OFF", command=update_label_text)
btnCameraToggle.pack(side="bottom", pady=22.5)
#
"""

# Close Button
# root.protocol("WM_DELETE_WINDOW", close_btn_msgbox)

# Run the Tkinter event loop
root.mainloop()
