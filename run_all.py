# tempral file to run video recording

from camcommands import cam_init, cam_non_identical, dev_info, dev_2_array, dev_set_param
from video_recording import video_recording
from multiprocessing import Process

if __name__ == "__main__":
    tl_factory, devices = cam_init()
    set_devices = cam_non_identical(devices, 2)
    dev_info(set_devices)
    cams = dev_2_array(tl_factory, set_devices, 2)

    param_dict = {"Height": 962, "Width": 1286, "ExposureTime": 2000, "FPS": 20}
    for cam in cams:
        dev_set_param(cam, param_dict)

    video_pos = {0:"front", 1:"side"}

    cam1 = Process(name="cam1", target=video_recording, 
                    args=("/Users/dkim/Desktop/basler_camera/recording", "test_multicore_%s.avi" % (video_pos[0]), cams[0]))
    cam2 = Process(name="cam2", target=video_recording, 
                    args=("/Users/dkim/Desktop/basler_camera/recording", "test_multicore_%s.avi" % (video_pos[1]), cams[1]))
    cam1.start()
    cam2.start()



