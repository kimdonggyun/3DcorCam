# script for video recording

from pypylon import pylon
from imageio import get_writer
from datetime import datetime
from threading import Thread
from tkinter import filedialog
import os
import cv2

class cam_preview:
    """
    preview set cameras with popup windows
    """
    def __init__(self, cams):

        cam1 = Thread(name="cam1", target= self.cam_preview_start, 
                        args=(cams[0], )
                        )
        cam2 = Thread(name="cam2", target= self.cam_preview_start, 
                        args=(cams[1], )
                        )
        cam1.start()
        cam2.start()
    
    def cam_preview_start(self, cam):
        """
        
        """



def cam_preview(cams):

    cam.Open()
    print("Set value: ", "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
        "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue())       
    cam.StartGrabbing()
    
    while cam.IsGrabbing():
        try :
            res = cam.RetrieveResult(10000, pylon.GrabStrategy_OneByOne )
        except:
            print("something wrong while retrieving the sequence")
        cv2.imshow("Cam", res.Array)
        res.Release()

            cam1 = Thread(name="cam1", target= self.video_recording_start, 
                        args=(filepaths[0] , cams[0], video_format, video_codec,
                        writing_mode, macro_block_size, quality, bitrate)
                        )
        cam2 = Thread(name="cam2", target= self.video_recording_start, 
                        args=(filepaths[1] , cams[1], video_format, video_codec,
                        writing_mode, macro_block_size, quality, bitrate)
                        )
        cam1.start()
        cam2.start()





class multi_video_recording_start:
    def __init__(self, cams, video_format = "FFMPEG", video_codec="h264",
                        writing_mode="I", macro_block_size= 2, quality=5, bitrate=None, fps=10):

        recording_dir = "/Users/dkim/Desktop/basler_camera/recording"
        filename_cam1 = input("type the file name for Cam1 :")
        filename_cam2 = input("type the file name for Cam2 :")
        filepath_cam1 = os.path.join(recording_dir, filename_cam1+str(".mp4"))
        filepath_cam2 = os.path.join(recording_dir, filename_cam2+str(".mp4"))

        filepaths = (filepath_cam1, filepath_cam2)

        self.multi_recording(filepaths=filepaths, cams=cams, video_format=video_format, video_codec=video_codec,
                                writing_mode=writing_mode, macro_block_size=macro_block_size, quality=quality,
                                bitrate=bitrate)

    def multi_recording(self, filepaths, cams, video_format = "FFMPEG", video_codec="h264",
                        writing_mode="I", macro_block_size= 1, quality=5, bitrate=None, fps=10):
        """
        recording cameras at the same time.
        filepaths (in tuple or list form with full file path and file name e.g. user/desktop/camer/video.mp4)
        cams (array of camera instaces)
        """

        cam1 = Thread(name="cam1", target= self.video_recording_start, 
                        args=(filepaths[0] , cams[0], video_format, video_codec,
                        writing_mode, macro_block_size, quality, bitrate)
                        )
        cam2 = Thread(name="cam2", target= self.video_recording_start, 
                        args=(filepaths[1] , cams[1], video_format, video_codec,
                        writing_mode, macro_block_size, quality, bitrate)
                        )
        cam1.start()
        cam2.start()

        print("recording start with %s at %s" % (cams[0].DeviceInfo.GetFriendlyName(), datetime.now()))
        print("recording start with %s at %s" % (cams[1].DeviceInfo.GetFriendlyName(), datetime.now()))
    
    """
    def get_filepath(self):

        filepath = filedialog.asksaveasfilename(initialdir=("C:/Users/dkim/Desktop/basler_cam/recording"), filetypes=[("video", "*.mp4")])
        print(filepath)
        return filepath
    """
    def video_recording_start(self, filepath, cam, video_format = "FFMPEG", video_codec="h264",
                    writing_mode="I", macro_block_size= 1, quality=5, bitrate=None, fps=10):
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

        with get_writer(filepath, format=video_format, codec=video_codec, 
                macro_block_size=macro_block_size, mode= writing_mode, quality=quality, bitrate=bitrate, fps=fps) as writer:

            cam.Open()
            print("Set value: ", "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
                "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue())       
            cam.StartGrabbing()
            
            while cam.IsGrabbing():
                try :
                    res = cam.RetrieveResult(10000, pylon.GrabStrategy_OneByOne )
                except:
                    print("something wrong while recording")
                writer.append_data(res.Array)
                res.Release()



class multi_video_recording_stop:
    # stop camera recording at the same time
    def __init__(self, cams):
        self.multi_recording_stop(cams)
        
    def multi_recording_stop(self, cams):
        # stop camera recording at the same time
        cam1 = Thread(name="cam1", target= self.video_recording_stop, 
                        args=(cams[0],)
                        )
        cam2 = Thread(name="cam2", target= self.video_recording_stop, 
                        args=(cams[1],)
                        )
        cam1.start() # start camera stopping
        cam2.start()

        cam1.join()
        cam2.join()

    def video_recording_stop(self, cam):
        # stopping video recording
        if cam.IsGrabbing():
            cam.StopGrabbing()
            cam.Close()
            print("recording finished with %s at %s" % (cam.DeviceInfo.GetFriendlyName(), datetime.now()))
        else:
            print("Cam %s is not currently recording" % (cam.DeviceInfo.GetFriendlyName()) )


