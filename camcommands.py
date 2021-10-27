# basic camera operation commands


# import packages and functions
import os
import sys
from pypylon import genicam
from pypylon import pylon
import datetime

def camOpen(camera):
    try:
        result = camera.Open()

        return camera
    except:
        return 0

def initiate_and_setup_cam(fps=24):
    # enable emulation 
    import os
    os.environ["PYLON_CAMEMU"] = "1"

    cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    cam.Open()
    cam.ImageFilename = img_dir
    cam.ImageFileMode = "On" # enable image file test pattern
    cam.TestImageSelector = "Off" # disable testpattern [ image file is "real-image"]
    cam.PixelFormat = "Mono8" # choose one pixel format. camera emulation does conversion on the fly

    cam.Height = height
    cam.Width = width
    
    cam.AcquisitionFrameRateAbs.SetValue(fps);
    
    return cam
