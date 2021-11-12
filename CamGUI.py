# GUI for camera control
# created by Dong-gyun Kim 
# contact dong-gyun.kim@awi.de

#import functions
import tkinter as tk
from tkinter import ttk
from camcommands import cam_init, dev_set_param
from video_recording import video_recording

class cam_control():
    def __init__(self):
        main_cam_GUI()


def main_cam_GUI():
    # this is the parent GUI of camera controlling
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
    button1 = ttk.Checkbutton(win, variable=var1, text="Get all connected Camera instaces and return as an Array")
    button1.place(relx=0.1, rely=0.3, anchor = "w")


    var2 = tk.BooleanVar()
    button2 = ttk.Checkbutton(win, variable=var2, text="Set Cameras' parameters")
    button2.place(relx=0.1, rely=0.4, anchor = "w")


    var3 = tk.BooleanVar()
    button3 = ttk.Checkbutton(win, variable=var3, text="Start or Stop Recording")
    button3.place(relx=0.1, rely=0.5, anchor = "w")


    """
    here run definitions
    
    """

    button4 = ttk.Button(win, text="run")
    button4.place(relx= 0.8, rely=0.8, anchor="n")

    win.mainloop() # appear all GUI setting as pop up window


def video_start_stop():
    # this is child GUI of main_cam_GUI when you want to control video starting and stopping
    win = tk.Tk()
    win.title("camera recording control")
    win.geometry("400x200")

    # add main sub lable
    lable = tk.Label(win, 
        text= "Start or Stop camera recording",
        font= ("Arial Bold", 15)
        )
    lable.place(relx=0.5, rely=0.05, anchor = "n")

    # add start and stop buttons

    button1 = ttk.Button(win, text="START")
    button1.place(relx= 0.3, rely=0.3, anchor="n")

    button2 = ttk.Button(win, text="STOP")
    button2.place(relx= 0.7, rely=0.3, anchor="n")


    

    win.mainloop() # appear all GUI setting as pop up window


def set_parameters():
    # this is child GUI of main_cam_GUI when you want to set new parameters on camera
    win = tk.Tk()
    win.title("Set Camera parameters")
    win.geometry("400x600")

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

    width_label = tk.Label(win, text='Width of Frame in Pixel :')
    width_label.place(relx = 0.1, rely = 0.4, anchor = 'w')
    width = tk.Entry(win, fg='black', width = 7)
    width.place(relx = 0.8, rely = 0.4, anchor = 'w')

    exposure_label = tk.Label(win, text='Exposure Time in µs :')
    exposure_label.place(relx = 0.1, rely = 0.5, anchor = 'w')
    exposure = tk.Entry(win, fg='black', width = 7)
    exposure.place(relx = 0.8, rely = 0.5, anchor = 'w')

    fps_label = tk.Label(win, text='FPS :')
    fps_label.place(relx = 0.1, rely = 0.6, anchor = 'w')
    fps = tk.Entry(win, fg='black', width = 7)
    fps.place(relx = 0.8, rely = 0.6, anchor = 'w')

    PixelFormat_label = tk.Label(win, text='PixelFormat (B/W: "Mono8") :')
    PixelFormat_label.place(relx = 0.1, rely = 0.7, anchor = 'w')
    PixelFormat = tk.Entry(win, fg='black', width = 7)
    PixelFormat.place(relx = 0.8, rely = 0.7, anchor = 'w')

    InterPacketDelay_label = tk.Label(win, text='Inter Packet Delay (default 20000) :')
    InterPacketDelay_label.place(relx = 0.1, rely = 0.8, anchor = 'w')
    InterPacketDelay = tk.Entry(win, fg='black', width = 7)
    InterPacketDelay.place(relx = 0.8, rely = 0.8, anchor = 'w')

    button = ttk.Button(win, text="ISERT")
    button.place(relx= 0.8, rely=0.9, anchor="n")

    win.mainloop() # appear all GUI setting as pop up window




if __name__=="__main__":
    #main_cam_GUI()
    #video_start_stop()
    #set_parameters()
    cam_control()
