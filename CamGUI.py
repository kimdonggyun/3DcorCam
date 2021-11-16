# GUI for camera control
# created by Dong-gyun Kim 
# contact dong-gyun.kim@awi.de

#import functions
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from camcommands import cam_init, multi_recording ,dev_set_param
from video_recording import video_recording

class cam_control():
    def __init__(self):
        print("Number of devices connected :")
        dev_number = input()
        self.cams = [0, 1] # for the test. remove this line later
        #self.cams = cam_init(dev_number)
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

        button4 = ttk.Button(win, text="run", command= run_func) # if arguments are in the command funtions lambda shuold be used. Otherwise, type in only function witout ()
        button4.place(relx= 0.8, rely=0.8, anchor="n")

        win.mainloop() # appear all GUI setting as pop up window


class set_parameter_entry:
    """
    setting camera paramters by typing the values on GUI
    """
    def __init__(self, cams):
        win = tk.Tk()
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
        height, width, exposure, fps =  self.height.get(), self.width.get(), self.exposure.get(), self.fps.get()
        PixelFormat, InterPacketDelay = self.PixelFormat.get(), self.InterPacketDelay.get()
        for cam in cams:
            dev_set_param (cam, Height = height , width = width, ExposureTime = exposure, FPS = fps, Pixelformat= PixelFormat, InterPacketDelay= InterPacketDelay )
        print(height, width, exposure, fps, PixelFormat, InterPacketDelay)
        self.win.destroy()



class video_start_stop_dir:
    def __init__(self, cams):
        # this is child GUI of main_cam_GUI when you want to control video starting and stopping
        win = tk.Tk()
        win.title("camera recording control")
        win.geometry("500x400")
        self.win = win

        # add main sub lable
        lable = tk.Label(win, 
            text= "Start or Stop camera recording",
            font= ("Arial Bold", 15)
            )
        lable.place(relx=0.5, rely=0.05, anchor = "n")

        # add cam1 and cam2 label
        cam1_label = tk.Label(win,
                        text = "here enter cam 1 name",
                        font = ("Arial Bold", 12)
                        )
        cam1_label.place(relx= 0.1, rely=0.2, anchor="w")

        cam2_label = tk.Label(win,
                        text = "here enter cam 2 name",
                        font = ("Arial Bold", 12)
                        )
        cam2_label.place(relx= 0.1, rely=0.3, anchor="w")

        # define functions for dir and filename entry
        def dir_sel():
            dir = filedialog.asksaveasfilename(initialdir=("C:/Users/dkim/Desktop/basler_cam/recording"), filetypes=[("video", "mp4")])
            print(dir)        
            return dir

        # add buttons for choosing directory and typing in file name
        cam1_button = tk.Button(win, text="choose directory", command=dir_sel)
        cam1_button.place(relx=0.6, rely= 0.2, anchor= "w") 

        cam2_button = tk.Button(win, text="choose directory", command=dir_sel)
        cam2_button.place(relx=0.6, rely= 0.3, anchor= "w")

        # add start and stop buttons
        button1 = ttk.Button(win, text="START", command= lambda: video_recording(dir , cams) )
        button1.place(relx= 0.3, rely=0.5, anchor="n")

        button2 = ttk.Button(win, text="STOP")
        button2.place(relx= 0.7, rely=0.5, anchor="n", command = lambda: video_recording_stop(cams))

        win.mainloop() # appear all GUI setting as pop up window


if __name__=="__main__":
    #main_cam_GUI()
    #video_start_stop()
    cam_control()
