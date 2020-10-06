""" MECHANICAL PARAMETERS """
s0_step_per_rev = 5760
s1_step_per_rev = 3200

# default_vel_mmps = 800.0
# default_accel_mmps2 = 40000.0
default_vel_mmps = 250.0
default_accel_mmps2 = 10000.0


""" OPERATION PARAMETERS """
gcode_folder = 'gcode'
audio_path = 'audio'
saveimg_path = '/home/pi/imgs'


""" CAMERA PARAMETERS """
IMAGE_RESOLUTION = (648,486)


""" OPENCV PARAMETERS """
TRACK_MODE = cv2.TrackerMOSSE_create
lock_on_size_px = (25,25)


""" FEATHER COMM PARAMETERS """
# Chars used for setting parameters on feather. All vars here must be int
Feather_Parameter_Chars = {
    'a': s0_arm_len_mm,
    'b': s1_arm_len_mm,
}

""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_ALL_FRAMES = True
