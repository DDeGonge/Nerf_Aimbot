__version__ = '0.1.0'

import time
import argparse
import Config as cfg
from SerialDevice import *
from MotorDriver import BottyMcBotFace
from CameraDriver import *
from Modes import *


def main():
    parser = argparse.ArgumentParser(description='HOLY HECK I made a robot that aims at stuff.')
    parser.add_argument('-m', type=int, default=0, help='Operational Mode - 0: Default, 1: First Face, 2: Loser')
    args = parser.parse_args()

    try:
        c = Camera()
        c.start()

        sd = SerialDevice()
        bot = BottyMcBotFace(sd)

        # Enable bot and move to center
        bot.zero()
        bot.enable()

        # Enter operational mode
        while True:
            if cfg.DEBUG_MODE:
                print('Starting...')
            bot.absolute_move(cfg.pitch_center_rads, cfg.yaw_center_rads)
            if args.m == 0:
                standard_mode(bot, c)
            elif args.m == 1:
                face_mode(bot, c)
            elif args.m == 2:
                standard_mode(bot, c, loser_mode=True)

                
    except Exception as e:
        c.stop()
        bot.disable()
        raise e

    finally:
        c.stop()
        bot.disable()


def track_and_save():
    c = Camera()
    c.start()
    

if __name__=='__main__':
    main()
