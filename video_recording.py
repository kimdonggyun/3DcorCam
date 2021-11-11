# script for video recording

from pypylon import pylon
from imageio import get_writer
import os
from datetime import datetime

def video_recording(file_dir, filename, cam, video_format = "FFMPEG", video_codec="h264",
                    writing_mode="I", macro_block_size= 1, quality=5, bitrate=None, fps = 15):
    """
    recording through camera and writing the video into as a video file
    video_format = e.g. FFMPEG
    filename should contain video_container = video container type e.g. filename.mp4
    video_codec = video codec e.g. h264
    writing_mode = "I" # imageio writing mode "I" for video recording
    macro_block_size = 1 # integer, width and height should be divisable with this number
    quality = 10  # float 0 - 10, default 5. better resolution with higher number
    bitrate = None  # integer, if None, quality parameter will be used. Otherwise, quality parameter will be ignored
    """

    with get_writer(os.path.join(file_dir, filename), format=video_format, codec=video_codec, 
            macro_block_size=macro_block_size, mode= writing_mode, fps=fps, quality=quality, bitrate=bitrate) as writer:
        #print("parent process : %s / process id %s" % (os.getppid(), os.getpid()))
        print("recording start with %s at %s" % (cam.DeviceInfo.GetFriendlyName(), datetime.now()))
        
        cam.Open()
        print("Set value: ", "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
            "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue())       
        cam.StopGrabbing()
        cam.StartGrabbingMax(500)
        print("cam %s is recording" %(cam.GetDeviceInfo().GetFriendlyName(), ))
        while cam.IsGrabbing():
            try :
                res = cam.RetrieveResult(10000, pylon.GrabStrategy_OneByOne )
            except:
                print("something wrong while recording")
            writer.append_data(res.Array)
            res.Release()

        cam.StopGrabbing()
        cam.Close()
        print("recording finish with %s at %s" % (cam.DeviceInfo.GetFriendlyName(), datetime.now()))