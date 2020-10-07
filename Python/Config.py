""" MECHANICAL PARAMETERS """
s0_step_per_rev = 27106
s1_step_per_rev = 27106

# default_vel_mmps = 800.0
# default_accel_mmps2 = 40000.0
default_vel_radps = 10
default_accel_radps2 = 100

pitch_travel_rads = 1
yaw_travel_rads = 1
pitch_center_rads = 0.5
yaw_center_rads = 0.5

half_press_index = 0
full_press_index = 1

trigger_min_pwm = 40
trigger_max_pwm = 120
trigger_hold_s = 0.5

loser_mode_bump_rads = 0.1
loser_mode_delay_s = 0.1

""" OPERATION PARAMETERS """
gcode_folder = 'gcode'
audio_path = 'audio'
saveimg_path = '/home/pi/imgs'


""" CAMERA PARAMETERS """
IMAGE_RESOLUTION = (640,480)
pixels_to_rads = 0.002


""" OPENCV PARAMETERS """
TRACK_MODE = "mosse"
lock_on_size_px = (50,50)


""" FEATHER COMM PARAMETERS """
# Chars used for setting parameters on feather. All vars here must be int
Feather_Parameter_Chars = {
    'a': s0_step_per_rev,
    'b': s1_step_per_rev,
    'c': default_vel_radps,
    'd': default_accel_radps2
}

""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_ALL_FRAMES = True
