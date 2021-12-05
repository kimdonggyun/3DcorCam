# basic camera operation commands

# import packages and functions
from pypylon import pylon

def cam_init (dev_number):
    """
    getting instance of basler cam
    return connected camera instances
    """
    print("getting the first camera instance")
    tl_factory = pylon.TlFactory.GetInstance() # get the first instance with all connected cameras
    devices = tl_factory.EnumerateDevices()

    dev_info(devices) # check whether cameras are connected

    set_tl_factory, set_devices = cam_non_identical(tl_factory, devices, dev_number) # check all physically conneceted cameras get instance

    cams = dev_2_array (set_tl_factory, set_devices, dev_number)

    return cams


def cam_non_identical (tl_factory, devices, dev_number):
    """
    Basler's package have a problem with MacOS and sometimes all connected camera doesn't show up.
    This def is created to check whether call camera's instants are created.
    Therefore, no duplicating camera instant.
    This function will be running untill you get certain number of camera instant you desire
    devices = initial camera instant
    dev_number = number of devices connected
    """
    
    if len(devices) == 0:
        raise pylon.RuntimeException("No camera connected, please check the camera connection!")

    else:
        temp_dev_list = [] # create empty camera list to com
        for dev_info in devices:
            temp_dev_list.append(dev_info.GetSerialNumber())
        
        if len(set(temp_dev_list)) == dev_number:
            print("all cameras' instance are created", temp_dev_list)
            return tl_factory, devices

        else:
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
            return tl_factory, devices

def dev_info(devices):
    """
    print out all connected cameras' basic information
    """
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
    """
    create array of devices connected for the easier handling of individual camera
    return array including device instance
    """
    cams = pylon.InstantCameraArray(min(len(devices), dev_number)) # create instant
    for i, cam in enumerate(cams):
        cam.Attach(tl_factory.CreateDevice(devices[i]))
    return cams
    
def dev_set_param (cam, Height = 962 , width = 1286, ExposureTime = 4000,
         FPS = 10, Pixelformat= "Mono8", InterPacketDelay= 10000, PacketSize = 1500):
    """
    when setting parameters while using multiple cameras, consider - Inter packet delay, Frame rate and Exposure Time
    which are critical for generating video (no dropped frame)
    """
    cam.Open() # open camera to change the parameter
    cam.UserSetSelector = "Default" # set camera parameters to dafault setting for constant result
    cam.UserSetLoad.Execute() # execute for factory setting
    
    print("original %s: " % (cam.GetDeviceInfo().GetFriendlyName(), ), " Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
            "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue(),
            "pixelformat:", cam.PixelFormat.GetValue(), "Inter Packet Dealy:", cam.GevSCPD.GetValue(), "Packet Size:", cam.GevSCPSPacketSize.GetValue() )
    
    # setting values from parameter dictionary
    cam.Height.SetValue(Height)
    cam.Width.SetValue(width)
    cam.ExposureTimeRaw.SetValue(ExposureTime)
    cam.AcquisitionFrameRateAbs.SetValue(FPS)
    cam.PixelFormat.SetValue(Pixelformat)
    cam.GevSCPD.SetValue(InterPacketDelay)
    cam.GevSCPSPacketSize.SetValue(PacketSize)

    print("Set %s: " %(cam.GetDeviceInfo().GetFriendlyName(), ) , "Height:",cam.Height.GetValue(), "Width:", cam.Width.GetValue(), 
            "Exposuretime:", cam.ExposureTimeRaw.GetValue(), "AcquisitionFrameRate:", cam.AcquisitionFrameRateAbs.GetValue(),
            "pixelformat:", cam.PixelFormat.GetValue(), "Inter Packet Dealy:", cam.GevSCPD.GetValue(), "Packet Size:", cam.GevSCPSPacketSize.GetValue())
    
    # Check whether maximum FPS with current setting is more than set FPS
    if float(cam.ResultingFrameRateAbs.GetValue()) >= FPS:
        print("You can apply set FPS (%s)" %(FPS  ,))
    else:
        print("maximum FPS is %s. Set lower FPS or change the setting" %(float(cam.ResultingFrameRateAbs.GetValue())  ,))
    
    cam.Close() # close camera
