import psutil
import os
import time
import threading

import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk


# variables
isCameraOn = True


# functions
def update_label_text():
    global isCameraOn

    isCameraOn = not isCameraOn

    if isCameraOn:
        btnCameraToggle['text'] = "Turn Camera OFF"
    else:
        btnCameraToggle['text'] = "Turn Camera ON"

    display_feed(isCameraOn)


def display_feed(camera_state):

    if camera_state == 1:
        cameraFeed.create_image(4, 4, image=placeholder_camOn, anchor="nw")
    else:
        cameraFeed.create_image(4, 4, image=placeholder_camOff, anchor="nw")


def close_btn_msgbox():
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        root.destroy()


# Create and initialize the main application window
root = tk.Tk()
img = tk.PhotoImage(file="res/pcbDefect.png")
root.minsize(1080, 600)
root.resizable(False, False)
root.title("pcbDefectProj")
root.iconphoto(False, img)


# Canvas
cameraFeed = tk.Canvas(root, borderwidth=2, relief="solid", bg="gray", height=500, width=1000)
cameraFeed.place(x=35, y=20)


# Camera Feed Placeholder
placeholder_camOn = ImageTk.PhotoImage(Image.open("res/camOn.png"))
placeholder_camOff = ImageTk.PhotoImage(Image.open("res/camOff.png"))


# adding image to feed
display_feed(isCameraOn)


# Toggle button
btnCameraToggle = ttk.Button(root, text="Turn Camera OFF", command=update_label_text)
btnCameraToggle.pack(side="bottom", pady=22.5)


# Close Button
root.protocol("WM_DELETE_WINDOW", close_btn_msgbox)


# Run the Tkinter event loop
root.mainloop()
