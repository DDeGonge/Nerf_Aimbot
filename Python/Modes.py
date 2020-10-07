from gpiozero import Button
from time import sleep
import Config as cfg

half_button = Button(cfg.half_press_index)
full_button = Button(cfg.full_press_index)

def standard_mode(bot, c, loser_mode=False):
    """ Half press trigger to lock on and track. Full press to fire """
    # Wait for button to be released if it started being held
    while half_button.is_held or full_button.is_held:
        pass

    # Wait unti half press is first triggered
    while not half_button.is_pressed:
        pass

    # Start tracking center frame
    c.lock_on()

    w_center_pix, h_center_pix = cfg.IMAGE_RESOLUTION
    w_center_pix = int(w_center_pix / 2)
    h_center_pix = int(h_center_pix / 2)

    # Stay in this tracking until trigger is released or shot is fired
    while half_button.is_held:
        h, w = c.get_location()
        x_move = (w - w_center_pix) * cfg.pixels_to_rads
        y_move = (h - h_center_pix) * cfg.pixels_to_rads
        bot.relative_move(x_move, y_move)

        if full_button.is_pressed:
            # It's fine don't look at this
            if loser_mode:
                bot.relative_move(cfg.loser_mode_bump_rads)
                sleep(cfg.loser_mode_delay_s)

            bot.trigger()
            c.reset_lock_on()
            return


def face_mode(bot, c):
    """ Will aim and fire at first face it sees as long as trigger is held """
    print('TODO')
