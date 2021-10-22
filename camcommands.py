# basic camera operation commands


# import packages and functions
import os
import sys
from pypylon import genicam
from pypylon import pylon

def camOpen(camera):
    try:
        result = camera.Open()

        return camera
    except:
        return 0
