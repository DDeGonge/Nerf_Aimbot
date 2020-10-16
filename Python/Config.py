""" MECHANICAL PARAMETERS """
s0_step_per_rev = 27106
s1_step_per_rev = 27106

pitch_travel_rads = 0.5
yaw_travel_rads = 1.2
pitch_center_rads = 0.21
yaw_center_rads = 0.59

default_vel_radps = 2.5
default_accel_radps2 = 20

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

loser_mode_bump_pixels = 20
loser_mode_delay_s = 0.5

face_mode_close_enough_pixels = 10


""" CAMERA PARAMETERS """
video_resolution = (640,480)
laser_center = (269,305)


""" OPENCV PARAMETERS """
tracking_mode = "mosse"  # NOT IMPLEMENTED
track_kp = 700
track_ki = 500
track_kd = 0
lock_on_size_px = (40,40)

lead_ahead_constant = 30  # pixels lead multiplier. Guess and check fam


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
