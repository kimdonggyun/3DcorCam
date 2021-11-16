# script for video recording

from pypylon import pylon
from imageio import get_writer
from datetime import datetime
from threading import Thread
from tkinter import filedialog


class multi_video_recording_start:
    def __init__(self, cams, video_format = "FFMPEG", video_codec="h264",
                        writing_mode="I", macro_block_size= 1, quality=5, bitrate=None, fps = 10):
        self.multi_recording(cams=cams, video_format=video_format, video_codec=video_codec,
                                writing_mode=writing_mode, macro_block_size=macro_block_size, quality=quality,
                                bitrate=bitrate, fps=fps)

    def multi_recording(self, cams, video_format = "FFMPEG", video_codec="h264",
                        writing_mode="I", macro_block_size= 1, quality=5, bitrate=None, fps = 10):
        # synchronized camera recording
        # get filepath for each camera
        cam1 = Thread(name="cam1", target= self.video_recording_start, 
                        args=(cams[0], video_format, video_codec,
                        writing_mode, macro_block_size, quality, bitrate, fps)
                        )
        cam2 = Thread(name="cam2", target= self.video_recording_start, 
                        args=(cams[1], video_format, video_codec,
                        writing_mode, macro_block_size, quality, bitrate, fps)
                        )
        cam1.start()
        cam2.start()


    def get_filepath(self):
        filepath = filedialog.asksaveasfilename(initialdir=("C:/Users/awiadm/Desktop/Dong_camera/recording"), filetypes=[("video", "*.mp4")])
        print(filepath)
        return filepath

    def video_recording_start(self, cam, video_format = "FFMPEG", video_codec="h264",
                    writing_mode="I", macro_block_size= 1, quality=5, bitrate=None, fps = 10):
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

        filepath = self.get_filepath() # get filepath to save using tkinter

        with get_writer(filepath, format=video_format, codec=video_codec, 
                macro_block_size=macro_block_size, mode= writing_mode, fps=fps, quality=quality, bitrate=bitrate) as writer:
            #print("parent process : %s / process id %s" % (os.getppid(), os.getpid()))
            print("recording start with %s at %s" % (cam.DeviceInfo.GetFriendlyName(), datetime.now()))
            
            cam.Open()
            print("Set value: ", "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
                "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue())       
            cam.StopGrabbing()
            cam.StartGrabbing()
            print("cam %s is recording" %(cam.GetDeviceInfo().GetFriendlyName(), ))
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
                        args=(cams[0])
                        )
        cam2 = Thread(name="cam2", target= self.video_recording_stop, 
                        args=(cams[1])
                        )
        cam1.start() # start camera stopping
        cam2.start()

        cam1.join()
        cam2.join()

    def video_recording_stop(self, cam):
        # stopping video recording
        cam.StopGrabbing()
        cam.Close()
        print("recording finished with %s at %s" % (cam.DeviceInfo.GetFriendlyName(), datetime.now()))


