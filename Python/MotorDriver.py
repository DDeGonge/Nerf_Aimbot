__version__ = '0.1.0'

import Config as cfg
import os
import time
import math

class BottyMcBotFace(object):
    def __init__(self, serial_device):
        self.serial_device = serial_device
        self.x_target = 0.
        self.y_target = 0.
        self.configure()
        self.is_parked = False

    """ Motion stuff """

    def configure(self):
        command_string = 'C0'
        for k, v in cfg.Feather_Parameter_Chars.items():
            command_string += ' {}{}'.format(k, v)
        self.serial_device.command(command_string)

    def home(self):
        print('TODO implement this plz')

    def zero(self):
        self.serial_device.command('G92 X0 Y0')

    def enable(self):
        self.serial_device.command('M17')

    def disable(self):
        self.serial_device.command('M84')

    def trigger(self, min_pwm = cfg.trigger_min_pwm, max_pwm = cfg.trigger_max_pwm, time_held_s = cfg.trigger_hold_s):
        self.serial_device.command('c1 a{} b{} c{}'.format(min_pwm, max_pwm, time_held_s))

    def absolute_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        # Calculate move
        self.x_target = xtar_mm
        self.y_target = ytar_mm

        command = 'G0 X{} Y{}'.format(xtar_mm, ytar_mm)
        if velocity_mmps is not None:
            command += ' F{}'.format(velocity_mmps * 60)
        self.serial_device.command(command)

    def relative_move(self, xtar_mm = 0, ytar_mm = 0, velocity_mmps = None):
        self.x_target += xtar_mm
        self.y_target += ytar_mm
        self.absolute_move(self.x_target, self.y_target, velocity_mmps)

    def send_gcode(self, filename):
        with open(os.path.join(cfg.gcode_folder, filename)) as f:
            while(True):
                line = f.readline().strip('\n')
                if not line:
                    break
                
                if line[0] == ';':
                    # Comments start with semicolon
                    continue

                self.serial_device.command(line)

    @property
    def is_homed(self):
        raise Exception('NOT IMPLEMENTED')

    @property
    def xpos_mm(self):
        ret = self.serial_device.command('M114')
        return float(ret.split(',')[0])

    @property
    def ypos_mm(self):
        ret = self.serial_device.command('M114')
        return float(ret.split(',')[1])
