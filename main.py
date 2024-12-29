import os
import threading
import cv2
import tkinter as tk
from tkinter import ttk, messagebox, Menu
from cv2_enumerate_cameras import enumerate_cameras
from PIL import Image, ImageTk

# Declaring/initializing variables
isCameraOn = False
currentCameraIndex = None
captureThread = None
stopEvent = threading.Event()

def on_closing():
    def background_exit():
        stop_camera_feed()
        root.after(0, root.destroy)

    # Ask for confirmation and exit in a background thread
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        exit_thread = threading.Thread(target=background_exit)
        exit_thread.daemon = True
        exit_thread.start()

def about_onclick():
    messagebox.showinfo("About", "About")

def start_camera_feed(camera_index):
    global currentCameraIndex, captureThread, stopEvent

    stop_camera_feed()  # Stop any existing camera feed

    currentCameraIndex = camera_index
    stopEvent.clear()

    captureThread = threading.Thread(target=update_camera_feed, args=(camera_index,))
    captureThread.daemon = True
    captureThread.start()

def stop_camera_feed():
    global stopEvent, captureThread, currentCameraIndex

    # Display black background immediately
    # root.after(0, display_black_background)

    # Stop the camera feed thread
    stopEvent.set()

    def background_cleanup():

        global captureThread, currentCameraIndex  # Corrected nonlocal usage

        # Release the camera immediately
        if currentCameraIndex is not None:
            cap = cv2.VideoCapture(currentCameraIndex)
            cap.release()

            clear_camera_feed()
            currentCameraIndex = None

        # Wait for the thread to finish in the background
        if captureThread and captureThread.is_alive():
            captureThread.join(timeout=2)
            if captureThread.is_alive():
                print("Thread failed to stop within timeout.")
            captureThread = None

    clear_camera_feed()

    # Run cleanup in a background thread
    cleanup_thread = threading.Thread(target=background_cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()


def clear_camera_feed():
    cameraFeed.delete("all")
    display_black_background()

def update_camera_feed(camera_index):
    global stopEvent

    cap = cv2.VideoCapture(camera_index)
    while not stopEvent.is_set() and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = frame.shape

        canvas_width = canvasWidth
        canvas_height = canvasHeight
        scale_width = canvas_width / frame_width
        scale_height = canvas_height / frame_height
        scale = max(scale_width, scale_height)

        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)
        frame = cv2.resize(frame, (new_width, new_height))

        offset_x = (new_width - canvas_width) // 2
        offset_y = (new_height - canvas_height) // 2
        frame = frame[offset_y:offset_y + canvas_height, offset_x:offset_x + canvas_width]

        root.after(0, update_canvas_image, frame)  # Thread-safe UI update
    cap.release()

def update_canvas_image(frame):
    img = ImageTk.PhotoImage(Image.fromarray(frame))
    cameraFeed.create_image(4, 4, anchor=tk.NW, image=img)
    cameraFeed.image = img

def display_black_background():
    cameraFeed.create_rectangle(4, 4, canvasWidth, canvasHeight, fill="black", outline="black")

# Initializing main application window
root = tk.Tk()

scrWidth = int(root.winfo_screenwidth() // 1.5)
scrHeight = int(root.winfo_screenheight() // 1.5)

canvasWidth = scrWidth - 20
canvasHeight = int(((canvasWidth / 16) * 9) - 10)

root.geometry(f"{scrWidth}x{scrHeight}+{scrWidth // 4}+{scrHeight // 4}")
root.resizable(False, False)
root.title("pcbDefectProj")

menubar = tk.Menu(root)
menu_properties = Menu(menubar, tearoff=0)
submenu_cameraSource = Menu(menu_properties, tearoff=0)

for camera_info in enumerate_cameras(cv2.CAP_MSMF):
    submenu_cameraSource.add_radiobutton(
        label=f'{camera_info.name}',
        command=lambda index=camera_info.index: start_camera_feed(index)
    )

submenu_cameraSource.add_radiobutton(label="camera_disable", command=stop_camera_feed)


menu_properties.add_cascade(label="Camera Source", menu=submenu_cameraSource)
menu_properties.add_separator()
menu_properties.add_command(label="About App...", command=about_onclick)
menu_properties.add_separator()
menu_properties.add_command(label="Close", command=on_closing)

menubar.add_cascade(label="Properties", menu=menu_properties)
root.config(menu=menubar)

cameraFeed = tk.Canvas(root, borderwidth=2, relief="solid", bg="black", height=canvasHeight, width=canvasWidth)
cameraFeed.place(x=5, y=5 + 5)

display_black_background()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()