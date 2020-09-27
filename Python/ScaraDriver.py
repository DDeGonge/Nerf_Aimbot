__version__ = '0.1.0'

import Config as cfg
import os
import time
import math

class Scara(object):
    def __init__(self, serial_device):
        self.serial_device = serial_device
        self.x_error = 0.
        self.y_error = 0.
        self.configure()
        self.update_defaults()
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

    def update_defaults(self, vel = None, acc = None):
        if acc == None:
            acc = cfg.default_accel_mmps2
        if vel == None:
            vel = cfg.default_vel_mmps
        self.serial_device.command('M201 a{} v{}'.format(acc, vel))

    def absolute_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        # Calculate move
        command = 'G0 X{} Y{}'.format(xtar_mm, ytar_mm)
        if velocity_mmps is not None:
            command += ' F{}'.format(velocity_mmps * 60)
        self.serial_device.command(command)

    def relative_move(self, xtar_mm, ytar_mm, velocity_mmps=None):
        raise Exception('NOT IMPLEMENTED')
        # return self.absolute_move(xpos_mm + xtar_mm, ypos_mm + ytar_mm, velocity_mmps)

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
        raise Exception('NOT IMPLEMENTED')

    @property
    def ypos_mm(self):
        raise Exception('NOT IMPLEMENTED')
