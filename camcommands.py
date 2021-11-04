# basic camera operation commands


# import packages and functions
from pypylon import pylon


def camOpen(camera):
    try:
        result = camera.Open()

        return camera
    except:
        return 0

def cam_init ():
    # getting instance of basler cam
    # return tl_factory and devices
    print("getting first camera instance")
    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices()
    return tl_factory, devices


def cam_non_identical (devices, dev_number):
    """
    Basler's package have a problem with MacOS and sometimes all connected camera doesn't show up.
    This def is created to check whether call camera's instants are created.
    Therefore, no duplicating camera instant.
    This function will be running untill you get certain number of camera instant you desire
    devices = initial camera instant
    dev_number = number of devices connected
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

def dev_info(devices):
    # print out all connected cameras' basic information
    # 2. check the devices information
    if len(devices) == 0:
        raise pylon.RuntimeException("No camera connected")
    else:
        print("total number of devices:", len(devices)) # print total number of devices connected
        for i, dev_info in enumerate(devices): # 
            if dev_info.GetDeviceClass() == 'BaslerGigE': # check if the connected cameras are GigE model. Otherwise software trigger won't work
                print("using %s as IP %s SN %s" % (dev_info.GetModelName(), dev_info.GetIpAddress() ,dev_info.GetSerialNumber()))
            else:
                raise EnvironmentError("no GigE device found")


def dev_2_array (tl_factory, devices, dev_number):
    # create array of devices connected for the easier handling of individual camera
    # return array including device instance
    cams = pylon.InstantCameraArray(min(len(devices), dev_number)) # create instant
    for i, cam in enumerate(cams):
        cam.Attach(tl_factory.CreateDevice(devices[i]))
    return cams


def dev_set_param (cam, param_dict):
    # set parameters of device individually
    # param_dict: paramter dictionary / param_dict = {"Height": , "Width": , "ExposureTime": , "FPS": }
    cam.Open() # cam open
    print("Setting device ", cam.GetDeviceInfo().GetFriendlyName())
    cam.Height.SetValue(param_dict["Height"])
    cam.Width.SetValue(param_dict["Width"])
    cam.ExposureTimeRaw.SetValue(param_dict["ExposureTime"])
    cam.AcquisitionFrameRateAbs.SetValue(param_dict["FPS"])
    print(cam.Height.GetValue(), cam.Width.GetValue(), cam.ExposureTimeRaw.GetValue(), cam.AcquisitionFrameRateAbs.GetValue())

    cam.Close() # close camera

