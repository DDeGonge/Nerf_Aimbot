""" MECHANICAL PARAMETERS """
s0_step_per_rev = 27106
s1_step_per_rev = 27106

pitch_travel_rads = 0.5
yaw_travel_rads = 1.2
pitch_center_rads = 0.21
yaw_center_rads = 0.59

default_vel_radps = 4
default_accel_radps2 = 40

trigger_min_pwm = 40
trigger_max_pwm = 120
trigger_hold_s = 0.5


""" PI PINOUTS """
half_press_index = 14
full_press_index = 15
laser_index = 17


""" OPERATION PARAMETERS """
gcode_folder = 'gcode'
audio_path = 'audio'
saveimg_path = '/home/pi/imgs'

loser_mode_bump_rads = 0.1
loser_mode_delay_s = 0.1


""" CAMERA PARAMETERS """
video_resolution = (640,480)
laser_center = (264,305)


""" OPENCV PARAMETERS """
tracking_mode = "mosse"  # NOT IMPLEMENTED
track_kp = 500
track_ki = 2
track_kd = 10
lock_on_size_px = (50,50)

vel_lowpass_filter = 0.8
lead_ahead_constant = 10  # pixels lead per rad/s velocity


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
SAVE_FRAMES = True
