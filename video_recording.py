# script for video recording

from pypylon import pylon
from imageio import get_writer
from datetime import datetime
from threading import Thread
import os, platform, cv2


class multi_video_recording_start:
    def __init__(self, cams, video_format = "FFMPEG", video_codec="h264",
                        writing_mode="I", macro_block_size= 2, quality=5, bitrate=None, fps=10):

        # check OS
        if platform.system() == "Windows":
            recording_dir = "C:/Users/awiadm/Desktop/Dong_camera/recording"
        elif platform.system() == "Darwin":
            recording_dir = "/Users/dkim/Desktop/basler_camera/recording"
        
        # input filepath
        filename_cam1 = input("type the file name for Cam1 :")
        filename_cam2 = input("type the file name for Cam2 :")
        filepath_cam1 = os.path.join(recording_dir, filename_cam1+str(".mp4"))
        filepath_cam2 = os.path.join(recording_dir, filename_cam2+str(".mp4"))

        filepaths = (filepath_cam1, filepath_cam2)

        # check fps of camera and set this value as viedeo writer's fps. Both Camera's set FPS and video writer's FPS value should have to be same!!
        cams[0].Open()
        cams[1].Open()

        while int(cams[0].AcquisitionFrameRateAbs.GetValue()) != int(cams[1].AcquisitionFrameRateAbs.GetValue()):
            print("cameras' FPS value is different. Set new FPS ")
            break

        cams[0].Close()
        cams[1].Close()

        # run multi_recording function
        self.multi_recording(filepaths=filepaths, cams=cams, video_format=video_format, video_codec=video_codec,
                                writing_mode=writing_mode, macro_block_size=macro_block_size, quality=quality,
                                bitrate=bitrate)

    def multi_recording(self, filepaths, cams, video_format = "FFMPEG", video_codec="h264",
                        writing_mode="I", macro_block_size= 2, quality=5, bitrate=None):
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

    def video_recording_start(self, filepath, cam, video_format = "FFMPEG", video_codec="h264",
                    writing_mode="I", macro_block_size= 2, quality=5, bitrate=None, fps=10):
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
        cam.Open() # open camera instance
        writer_fps = int(cam.AcquisitionFrameRateAbs.GetValue()) # get fps value from camera to apply on writer's fps

        with get_writer(filepath, format=video_format, codec=video_codec, 
                macro_block_size=macro_block_size, mode= writing_mode, quality=quality, bitrate=bitrate, fps=writer_fps) as writer:

            print("Set value: ", "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
                "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue())       
            cam.StartGrabbing()
            
            while cam.IsGrabbing():
                try :
                    res = cam.RetrieveResult(10000)
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
            cam.Release()
            print("recording finished with %s at %s" % (cam.DeviceInfo.GetFriendlyName(), datetime.now()))
        else:
            print("Cam %s is not currently recording" % (cam.DeviceInfo.GetFriendlyName()) )


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
        print("Preview will start soon. To quit the preview, press 'q' for each windows")
        cam1 = Thread(name="cam1", target= self.video_stream, args=(cams[0], ) )
        cam2 = Thread(name="cam2", target= self.video_stream, args=(cams[1], ) )
        cam1.start()
        cam2.start()

    def video_stream(self, cam):
        cam.Open() # cam open
        print("Set %s: " %(cam.GetDeviceInfo().GetFriendlyName(), ) , "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
        "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue(),
        "pixelformat:", cam.PixelFormat.GetValue(), "Inter Packet Dealy:", cam.GevSCPD.GetValue())

        cam.StartGrabbing() # cam start getting image
        print("cam %s is showing" % (cam.DeviceInfo.GetFriendlyName() , ))
        while cam.IsGrabbing():
            try:
                res = cam.RetrieveResult(10000)
            except:
                print("something wrong while retrieving the sequence")
            
            img_ary = res.Array # array of image
            if img_ary.size == 0:
                print("no image")
            else:
                cv2.imshow("cam %s" % (cam.DeviceInfo.GetFriendlyName() ,), img_ary)
                cv2.namedWindow("cam %s" % (cam.DeviceInfo.GetFriendlyName() ,), cv2.WINDOW_NORMAL)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("prevewing is done")
                    cam.StopGrabbing()
                    cam.Close()
                    cv2.destroyWindow("cam %s" % (cam.DeviceInfo.GetFriendlyName() ,)) # destroy popup window, Mendatory for the multiple previewing
                    break
