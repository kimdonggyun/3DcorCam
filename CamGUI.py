# GUI for camera control
# created by Dong-gyun Kim 
# contact dong-gyun.kim@awi.de

#import functions
import tkinter as tk
from tkinter import Toplevel, ttk
from camcommands import cam_init, dev_set_param
from video_recording import multi_video_recording_start, multi_video_recording_stop

import tkinter as tk
from tkinter import ttk, Frame, Label
from datetime import datetime
from threading import Thread
from PIL import ImageTk, Image # packages for preview tkinter
import cv2


class cam_control():
    def __init__(self):
        print("Number of devices connected :")
        dev_number = int(input()) # default input data type is string. Should chage the type with desire type
        self.cams = cam_init(dev_number)
        self.main_cam_GUI()

    def main_cam_GUI(self):
        # this is the parent GUI of controlling camera
        win = tk.Tk()
        win.title("Machine Vison Camera controlling")
        win.geometry("500x500")

        # add main sub lable
        lable = tk.Label(win, 
            text= "Choose Button(s) to run Action(s)",
            font= ("Arial Bold", 20)
            )
        lable.place(relx=0.5, rely=0.05, anchor = "n")

        # add action buttons
        var1 = tk.BooleanVar()
        button1 = ttk.Checkbutton(win, variable=var1, text="Get all connected Cameras' instace and return as an Array")
        button1.place(relx=0.1, rely=0.3, anchor = "w")

        var2 = tk.BooleanVar()
        button2 = ttk.Checkbutton(win, variable=var2, text="Set Cameras' parameters")
        button2.place(relx=0.1, rely=0.4, anchor = "w")

        var3 = tk.BooleanVar()
        button3 = ttk.Checkbutton(win, variable=var3, text="Start or Stop Recording")
        button3.place(relx=0.1, rely=0.5, anchor = "w")

        var4 = tk.BooleanVar()
        button4 = ttk.Checkbutton(win, variable=var4, text="Previe camera")
        button4.place(relx=0.1, rely=0.6, anchor = "w")

        # add functions for each buttons
        def run_func():
            if var1.get(): # var1 = getting camera instance and return as an array
                print("Getting all connected cameras instance")
                cams = cam_init()
                print("Cameras' instance ", cams)
                return cams
            if var2.get(): # var2 = setting cameras' parameters
                print("Setting cameras' parameter")
                set_parameter_entry(self.cams) # call a GUI to type in parameters and return this values
            if var3.get(): # var3 = starting and stopping camera record
                print("Start or Stop camera recording")
                video_start_stop_dir(self.cams) # call a GUI to start or stop video recording
            if var4.get():
                print("Previewing camera")
                cam_preview(self.cams)

        run_button = ttk.Button(win, text="run", command= run_func) # if arguments are in the command funtions lambda shuold be used. Otherwise, type in only function witout ()
        run_button.place(relx= 0.8, rely=0.8, anchor="n")

        win.mainloop() # appear all GUI setting as pop up window

class cam_preview:
    """
    preview set cameras with popup windows
    """
    def __init__(self, cams):
        self.cam_preview_start(cams)
    
    def cam_preview_start(self, cams):
        """
        previewing currently connected camera
        """
        cam1 = Thread(name="cam1", target= self.video_stream, args=(cams[0], ) )
        cam2 = Thread(name="cam2", target= self.video_stream, args=(cams[1], ) )
        cam1.start()
        cam2.start()

    def video_stream(self, cam):
        cam.Open() # cam open
        cam.StartGrabbing() # cam start getting image
        while cam.IsGrabbing():
            try:
                res = cam.RetrieveResult(10000)
            except:
                print("something wrong while retrieving the sequence")
        print("cam %s is showing" % (cam.DeviceInfo.GetFriendlyName() , ))
        img_ary = res.Array
        cv2.imshow("cam %s" % (cam.DeviceInfo.GetFriendlyName() ,), img_ary)
        cv2.namedWindow("cam %s" % (cam.DeviceInfo.GetFriendlyName() ,))





"""
class cam_preview:
    
    preview set cameras with popup windows
    
    def __init__(self, cams):
        self.cam_preview_start(cams)
    
    def cam_preview_start(self, cams):
        
        previewing currently connected camera
        
        cam1 = Thread(name="cam1", target= self.video_stream, args=(cams[0], ) )
        cam2 = Thread(name="cam2", target= self.video_stream, args=(cams[1], ) )
        cam1.start()
        cam2.start()

    def video_stream(self, cam):
        win = tk.Tk()
        app = Frame(win, bg="white")
        app.grid()
        # Create a label in the frame
        lmain = Label(app)
        lmain.grid()

        win.title("Previewing camera %s" % (cam.DeviceInfo.GetFriendlyName() , ))
        win.geometry("1000x1000")

        cam.Open()
        cam.StartGrabbing()

        while cam.IsGrabbing():
            try:
                res = cam.RetrieveResult(10000)
            except:
                print("something wrong while retrieving the sequence")
            
            image = Image.fromarray(res.Array)
            imgtk = ImageTk.PhotoImage(image=image)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain(1, self.video_stream)

        win.mainloop()
"""      

class set_parameter_entry:
    """
    setting camera paramters by typing the values on GUI
    """
    def __init__(self, cams):
        win = Toplevel
        win.title("Set Camera parameters")
        win.geometry("450x600")
        self.win = win

        # add main sub lable
        lable = tk.Label(win, 
            text= "type camera parameters",
            font= ("Arial Bold", 15)
            )
        lable.place(relx=0.5, rely=0.05, anchor = "n")

        # set enntry
        height_label = tk.Label(win, text='Height of Frame in Pixel :')
        height_label.place(relx = 0.1, rely = 0.3, anchor = 'w')
        height = tk.Entry(win, fg='black', width = 7)
        height.place(relx = 0.8, rely = 0.3, anchor = 'w')
        self.height = height

        width_label = tk.Label(win, text='Width of Frame in Pixel :')
        width_label.place(relx = 0.1, rely = 0.4, anchor = 'w')
        width = tk.Entry(win, fg='black', width = 7)
        width.place(relx = 0.8, rely = 0.4, anchor = 'w')
        self.width = width

        exposure_label = tk.Label(win, text='Exposure Time in µs :')
        exposure_label.place(relx = 0.1, rely = 0.5, anchor = 'w')
        exposure = tk.Entry(win, fg='black', width = 7)
        exposure.place(relx = 0.8, rely = 0.5, anchor = 'w')
        self.exposure = exposure

        fps_label = tk.Label(win, text='FPS :')
        fps_label.place(relx = 0.1, rely = 0.6, anchor = 'w')
        fps = tk.Entry(win, fg='black', width = 7)
        fps.place(relx = 0.8, rely = 0.6, anchor = 'w')
        self.fps = fps

        PixelFormat_label = tk.Label(win, text='PixelFormat (B/W: "Mono8") :')
        PixelFormat_label.place(relx = 0.1, rely = 0.7, anchor = 'w')
        PixelFormat = tk.Entry(win, fg='black', width = 7)
        PixelFormat.place(relx = 0.8, rely = 0.7, anchor = 'w')
        self.PixelFormat = PixelFormat

        InterPacketDelay_label = tk.Label(win, text='Inter Packet Delay (default 20000) :')
        InterPacketDelay_label.place(relx = 0.1, rely = 0.8, anchor = 'w')
        InterPacketDelay = tk.Entry(win, fg='black', width = 7)
        InterPacketDelay.place(relx = 0.8, rely = 0.8, anchor = 'w')
        self.InterPacketDelay = InterPacketDelay

        button = ttk.Button(win, text="ISERT", command= lambda: self.run_button (cams))
        button.place(relx= 0.8, rely=0.9, anchor="n")

        win.mainloop() # appear all GUI setting as pop up window

    def run_button(self, cams):
        height, width, exposure, fps =  int(self.height.get()), int(self.width.get()), int(self.exposure.get()), int(self.fps.get())
        PixelFormat, InterPacketDelay = str(self.PixelFormat.get()), int(self.InterPacketDelay.get())
        print(height, width, exposure, fps, PixelFormat, InterPacketDelay)
        for cam in cams:
            dev_set_param (cam, Height = height , width = width, ExposureTime = exposure, FPS = fps, Pixelformat= PixelFormat, InterPacketDelay= InterPacketDelay )
        
        self.win.destroy()



class video_start_stop_dir:
    def __init__(self, cams):
        # this is child GUI of main_cam_GUI when you want to control video starting and stopping
        win = tk.Tk()
        win.title("camera recording control")
        win.geometry("400x300")
        self.win = win

        # add main sub lable
        lable = tk.Label(win, text= "Start or Stop camera recording", font= ("Arial Bold", 15) )
        lable.place(relx=0.5, rely=0.05, anchor = "n")

        # add start and stop buttons
        button1 = ttk.Button(win, text="START", command= lambda: multi_video_recording_start(cams) )
        button1.place(relx= 0.3, rely=0.5, anchor="n")

        button2 = ttk.Button(win, text="STOP", command = lambda: multi_video_recording_stop(cams))
        button2.place(relx= 0.7, rely=0.5, anchor="n")

        win.mainloop() # appear all GUI setting as pop up window


if __name__=="__main__":

    cam_control()
