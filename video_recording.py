# script for video recording

from pypylon import pylon
from imageio import get_writer
import os
from datetime import datetime

def video_recording(file_dir, filename, caminstance):
    with get_writer(os.path.join(file_dir, filename)) as writer:
        print("parent process : %s / process id %s" % (os.getppid(), os.getpid()))
        print("recording start with %s at %s" % (caminstance.DeviceInfo.GetFriendlyName(), datetime.now()))
        caminstance.StopGrabbing()
        caminstance.StartGrabbingMax(500)
        while caminstance.IsGrabbing():
            try :
                res = caminstance.RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
            except:
                print("something wrong while recording")
            writer.append_data(res.Array)
            res.Release()
        print("recording finish with %s at %s" % (caminstance.DeviceInfo.GetFriendlyName(), datetime.now()))