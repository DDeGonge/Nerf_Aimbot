#include "nerfy.h"
#include "funks.h"

#define Serial SERIAL_PORT_USBVIRTUAL

void setup()
{
  // Init serial, sd, musicplayer, and neopixel
  Serial.begin(250000);
  while (!Serial) { delay(1); }
  pixel.begin();
}

void loop()
{
  // Initialize some stuff
  setLEDColor(200, 0, 0);
  unsigned long startTime_us = micros();
  unsigned long t_elapsed_us;
  Servo pen_servo;
  pen_servo.attach(servo_pin);
  stepper s0(s0_step, s0_dir, s0_en, false);
  stepper s1(s1_step, s1_dir, s1_en, false);

  char serial_data[MAX_MSG_LEN];
  setLEDColor(100, 0, 0);

  // Init vars
  char base_cmd, char_value;
  int32_t base_value, int_value;
  float float_value;

  // Start main response loop
  while (true)
  {
    s0.step_if_needed();
    s1.step_if_needed();
//    delay(10);

    t_elapsed_us = micros() - startTime_us;
    clear_data(serial_data);
    if (respondToSerial(serial_data)) 
    {
      setLEDColor(100, 50, 0);

      // Parse input into data chunks
      vector<string> args;
      parse_inputs(serial_data, args);
      parse_int(args[0], base_cmd, base_value);

      switch (tolower(base_cmd)) 
      {
        case 'g': {
          switch (base_value) 
          {
            case 0:
            case 1: {
              // LINEAR MOVE DO NOT WAIT
              float xpos, ypos, feedrate;
              gcode_command_floats gcode(args);
              if(gcode.com_exists('x'))
                s0.set_rad_target(gcode.fetch('x'), gcode.fetch('f'));
              if(gcode.com_exists('y'))
                s1.set_rad_target(gcode.fetch('y'), gcode.fetch('f'));
              break;
            }
            case 28: {
              Serial.println("TODO homing");
              break;
            }
            case 92: {
              // Overwrite current pos
              gcode_command_floats gcode(args);
              if(gcode.com_exists('x'))
                s0.set_rad_target(gcode.fetch('x'), gcode.fetch('f'));
              if(gcode.com_exists('y'))
                s1.set_rad_target(gcode.fetch('y'), gcode.fetch('f'));
              break;
            }
          }
          break;
        }
      case 'm': {
          switch (base_value) 
          {
            case 17: {
              // Enable Steppers
              gcode_command_floats gcode(args);
              if(gcode.com_exists('x'))
                s0.enable();
              if(gcode.com_exists('y'))
                s1.enable();
              break;
            }
            case 84: {
              // Disable Steppers
              gcode_command_floats gcode(args);
              if(gcode.com_exists('x'))
                s0.disable();
              if(gcode.com_exists('y'))
                s1.disable();
              break;
            }
            case 114: {
              // Get current position
//              float xpos, ypos;
//              bot.get_pos(xpos, ypos);
//              Serial.println("TODO FINISH THIS ONE");
              break;
            }
            case 201: {
              // Set Acceleration Limits
//              gcode_command_floats gcode(args);
//              bot.set_def_speeds(gcode.fetch('a'), gcode.fetch('v'));
              break;
            }
          }
          break;
        }
      case 'c': {
          switch (base_value) 
          {
            case 0: {
              // configure hardware stuff
//              gcode_command_floats gcode(args);
//              bot.configure(gcode.fetch('a'), gcode.fetch('b'), gcode.fetch('c'), gcode.fetch('d'), gcode.fetch('e'), gcode.fetch('f'), gcode.fetch('g'), gcode.fetch('h'));
              break;
            }
          }
        }
        break;
      }
      Serial.println("ok");
      setLEDColor(0, 100, 0);
    }
  }
}
