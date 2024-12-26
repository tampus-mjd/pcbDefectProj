import os
import time
import threading
import ctypes

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, Menu
from cv2_enumerate_cameras import enumerate_cameras

import cv2

from PIL import Image, ImageTk

# TODO: implement camera interface function

# Declaring/initializing variables
isCameraOn = False
cameraCounter = 0


# Declaring/initializing variables
def on_closing():
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        root.destroy()


def about_onclick():
    messagebox.showinfo("About", "About")

# def open_camera(camera_index):


# Initializing main application window
root = Tk()

scrWidth = (root.winfo_screenwidth() // 1.5)
scrHeight = (root.winfo_screenheight() // 1.5)

# img = tk.PhotoImage(file="res/pcbDefect.png")

# Initializing window parameters
root.geometry("%dx%d+%d+%d" % (scrWidth, scrHeight, (scrWidth // 4), (scrHeight // 4)))
root.resizable(False, False)
root.title("pcbDefectProj")
# root.iconphoto(False, img)

# Initializing Menu bar
menubar = tk.Menu(root)

menu_properties = Menu(menubar, tearoff=0)

submenu_cameraSource = Menu(menu_properties, tearoff=0)

for camera_info in enumerate_cameras(cv2.CAP_MSMF):
    cameraCounter += 1
    submenu_cameraSource.add_radiobutton(label=f'{camera_info.name}', command='')
    print(f'{camera_info.index}: {camera_info.name}')

# submenu_cameraSource.add_radiobutton(label="source1", command='')
# submenu_cameraSource.add_radiobutton(label="source2", command='')
submenu_cameraSource.add_separator()
submenu_cameraSource.add_command(label="camera_disable", command='')

menu_properties.add_cascade(label="Camera Source", menu=submenu_cameraSource)

menu_properties.add_separator()
menu_properties.add_command(label="About App...", command=about_onclick)
menu_properties.add_separator()
menu_properties.add_command(label="Close", command=on_closing)

menubar.add_cascade(label="Properties", menu=menu_properties)

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
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
root.mainloop()


"""
import cv2
from cv2_enumerate_cameras import enumerate_cameras

for camera_info in enumerate_cameras(cv2.CAP_MSMF):
    print(f'{camera_info.index}: {camera_info.name}')
"""