# tempral file to run video recording

from camcommands import cam_init, cam_non_identical, dev_info, dev_2_array, dev_set_param
from video_recording import video_recording
from threading import Thread

if __name__ == "__main__":
    cams = cam_init(2)

    for cam in cams:
        dev_set_param(cam) # with default setting

    video_pos = {0:cams[0].DeviceInfo.GetFriendlyName() , 1:cams[1].DeviceInfo.GetFriendlyName()}

    cam1 = Thread(name="cam1", target=video_recording, 
                    args=("C:/Users/dkim/Desktop/basler_cam/recording", "test_withpy_%s.mp4" % (video_pos[0]), cams[0]))
    cam2 = Thread(name="cam2", target=video_recording, 
                    args=("C:/Users/dkim/Desktop/basler_cam/recording", "test_withpy_%s.mp4" % (video_pos[1]), cams[1]))
    cam1.start()
    cam2.start()

    cam1.join()
    cam2.join()