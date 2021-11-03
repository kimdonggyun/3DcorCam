# 3DcorCam
# communication with Basler Cam

The main purpose of this respository is to manage the machine vision camera, especially from BASLER.
Here, multi-camera handling method is included.
For someone has a camera moddule supporting "Action Commands", please refer Pylon's "Action Commands" method which is possibly the best way to handle multiple cameras.
Otherwise, the camera module does not support "Action Commands", try using "MultiProcessing" or "MultiThreading".

Requirement

python -version 3.7.X
pypylon
