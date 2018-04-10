import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import json
from time import sleep
PI = False
RESOLUTIONX = 640
RESOLUTIONY = 480
COLOURS = (
    "RAINBOW_BLUE",
    "RAINBOW_RED",
    "RAINBOW_GREEN",
    "RAINBOW_YELLOW"
    )
FILENAME = "thresholds.json"
if PI:
    import picamera
    import picamera.array
    class Camera:
        def __init__(self, *args, **kwargs):
            self.camera = picamera.PiCamera(*args, **kwargs)
            self.camera.resolution = (RESOLUTIONX, RESOLUTIONY)
            self.camera.rotation = 0
            # Set ISO to the desired value
            self.camera.iso = 200
            # Wait for the automatic gain control to settle
            sleep(2)
            # Now fix the values
            self.camera.shutter_speed = self.camera.exposure_speed
            self.camera.exposure_mode = 'off'
            g = self.camera.awb_gains
            self.camera.awb_mode = 'off'
            self.camera.awb_gains = g
        def capture(self):
            with picamera.array.PiRGBArray(self.camera) as stream:
                self.camera.capture(stream, format='bgr')
                # At this point the image is available as stream.array
                image = stream.array
            return image
else:
    class Camera:
        def __init__(self):
            self.cap = cv2.VideoCapture(0)

        def capture(self):
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            return frame

class ThresholdAdjuster(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.initWidgets()
        self.update_frames()

    def initWidgets(self):
        self.cleanImgLbl = tk.Label(self)
        self.cleanImgLbl.grid(row=0, column=0)

        self.maskImgLbl = tk.Label(self)
        self.maskImgLbl.grid(row=0, column=1, columnspan=2)

        self.hmin_scale = tk.Scale(self, from_=0, to=180, orient=tk.HORIZONTAL)
        self.hmin_scale.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

        self.smin_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL)
        self.smin_scale.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

        self.vmin_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL)
        self.vmin_scale.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

        self.hmax_scale = tk.Scale(self, from_=0, to=180, orient=tk.HORIZONTAL)
        self.hmax_scale.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S, columnspan=2)

        self.smax_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL)
        self.smax_scale.grid(row=2, column=1, sticky=tk.W+tk.E+tk.N+tk.S, columnspan=2)

        self.vmax_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL)
        self.vmax_scale.grid(row=3, column=1, sticky=tk.W+tk.E+tk.N+tk.S, columnspan=2)

        self.colour_selection = tk.StringVar()
        self.colour_selection.set(COLOURS[0])
        self.colour_selection.trace("w", self.update_buttons)
        self.colour_selector = tk.OptionMenu(*(self, self.colour_selection) + tuple(COLOURS))
        self.colour_selector.grid(row=4, column=0)

        self.load_button = tk.Button(self, command=self.load_thresh, text="LOAD")
        self.load_button.grid(row=4, column=1)

        self.save_button = tk.Button(self, command=self.save_thresh, text="SAVE")
        self.save_button.grid(row=4, column=2)

        self.update_buttons()
        self.capture = Camera()
        
    def update_frames(self):
        thresholds = np.array([
            [
                self.hmin_scale.get(),
                self.smin_scale.get(),
                self.vmin_scale.get()
            ],
            [
                self.hmax_scale.get(),
                self.smax_scale.get(),
                self.vmax_scale.get()
            ]
        ])
            
        frame = self.capture.capture()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.cleanImgLbl.imgtk = imgtk
        self.cleanImgLbl.configure(image=imgtk)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, thresholds[0], thresholds[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        img = Image.fromarray(mask)
        imgtk = ImageTk.PhotoImage(image=img)
        self.maskImgLbl.imgtk = imgtk
        self.maskImgLbl.configure(image=imgtk)
        
        self.cleanImgLbl.after(10, self.update_frames)

    def update_buttons(self, *args):
        with open(FILENAME, 'r') as f:
            obj = json.load(f)
        if self.colour_selection.get() in obj:
            self.load_button.configure(state=tk.NORMAL)
        else:
            self.load_button.configure(state=tk.DISABLED)

    def load_thresh(self):
        with open(FILENAME, 'r') as f:
            obj = json.load(f)
        n = obj[self.colour_selection.get()]
        self.hmin_scale.set(n[0][0])
        self.smin_scale.set(n[0][1])
        self.vmin_scale.set(n[0][2])

        self.hmax_scale.set(n[1][0])
        self.smax_scale.set(n[1][1])
        self.vmax_scale.set(n[1][2])

    def save_thresh(self):
        with open(FILENAME, 'r') as f:
            obj = json.load(f)
        new_obj = {
            self.colour_selection.get(): [
            [
                self.hmin_scale.get(),
                self.smin_scale.get(),
                self.vmin_scale.get()
            ],
            [
                self.hmax_scale.get(),
                self.smax_scale.get(),
                self.vmax_scale.get()
            ]
        ]
            }
        print(new_obj)
        print(type(self.colour_selection.get()))
        print(type(self.smin_scale.get()))
        obj.update(new_obj)
        with open(FILENAME, 'w') as f:
            json.dump(obj, f)
        

root = tk.Tk()
root.title("Threshold Tuner")
gui = ThresholdAdjuster(root)
gui.grid()
root.mainloop()
