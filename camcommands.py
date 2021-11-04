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

def cam_non_identical (devices, dev_number):
    """
    Basler's package have a problem with MacOS and sometimes all connected camera doesn't show up.
    This def is created to check whether call camera's instants are created.
    Therefore, no duplicating camera instant.
    This function will be running untill you get certain number of camera instant you desire
    devices = initial camera instant
    """
    temp_dev_list = [] # create empty camera list to com
    if len(devices) == 0:
        raise pylon.RuntimeException("No camera connected, please check the camera connection!")
    else:
        for dev_info in devices:
            temp_dev_list.append(dev_info.GetSerialNumber())
        while len(set(temp_dev_list)) != dev_number: # count the unique camera instant and compare it with desired number of cameras
            tl_factory = pylon.TlFactory.GetInstance() # get instance again
            devices = tl_factory.EnumerateDevices()
            temp_dev_list = []
            for dev_info in devices:
                temp_dev_list.append(dev_info.GetSerialNumber())
            print(temp_dev_list)
            if len(set(temp_dev_list)) == dev_number:
                print("all cameras' instance are created", temp_dev_list)
                break
    return devices


def cam_init ():
    # 
