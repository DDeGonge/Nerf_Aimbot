/* STEPPER STUFF */

stepper::stepper(int s_pin, int d_pin, int e_pin, bool rev)
{
  pinMode(s_pin, OUTPUT);
  pinMode(d_pin, OUTPUT);
  pinMode(e_pin, OUTPUT);
  step_pin = s_pin;
  dir_pin = d_pin;
  en_pin = e_pin;
  reverse = rev;
  current_velocity = 0;
  current_step_count = 0;
  disable();
}

// Public - enable stepper motor
void stepper::enable()
{
  digitalWrite(en_pin, LOW);
}

// Public - disable stepper motor
void stepper::disable()
{
  digitalWrite(en_pin, HIGH);
}

// Public - Update stepper parameters. Feed NOVALUE to not change any particular parameter
void stepper::update_config(int32_t steps_per_rev_new, float max_vel_new, float max_accel_new)
{
  if (max_vel_new != NOVALUE)
    max_vel = max_vel_new;
  if (max_accel_new != NOVALUE)
    max_accel = max_accel_new;
  if (steps_per_rev_new != NOVALUE)
  {
    steps_per_rev = steps_per_rev_new;
    step_size_rads = 2 * PI / steps_per_rev;
  }
}

// Public - Overwrite the current position to be any rad value designated
void stepper::set_current_rads(double target)
{
  target = target == NOVALUE ? 0 : target;
  double working_count = target * steps_per_rev;
  working_count /= (2 * PI);
  working_count += 0.4999; // For the rounding
  current_step_count = (int32_t) working_count;
}

// Public - Update target position in rads. Respects any joint momentum.
void stepper::set_rad_target(double target, float feedrate)
{
  target_rads = target;
  next_step_us = micros();
  if (feedrate != NOVALUE)
    max_vel = feedrate;
}

// Public - The magic sauce. Tracks motor motion and calculates if a step is needed now to stay on track.
bool stepper::step_if_needed()
{
  uint32_t t_now = micros();
  int32_t step_target = (steps_per_rev * target_rads);
  step_target /= 2 * PI;

  // Check if motor is in right place already
  if((abs(current_velocity) < 0.001) && (step_target == current_step_count))
    return false;
  else if((abs(current_velocity) < 0.001) && (current_step_count > step_target))
    set_dir(false);
  else if((abs(current_velocity) < 0.001) && (current_step_count < step_target))
    set_dir(true);
  
  if(micros() > next_step_us)
  {
    take_step();

    uint32_t cur_step_us = next_step_us;
    double stop_dist_rads = pow(current_velocity, 2) / (max_accel);
    double stop_pos_rads = (current_step_count * 2 * PI) / steps_per_rev;

//    Serial.println(stop_pos_rads);
//    Serial.print("\t stop_dist_rads: ");
//    Serial.print(stop_dist_rads);
//    Serial.print("\t stop_pos_rads: ");
//    Serial.print(stop_pos_rads);
//    Serial.print("\t");

    // This mess determines if we need to slow down
    if((current_dir && ((stop_pos_rads + stop_dist_rads) > target_rads)) || (!current_dir && ((stop_pos_rads - stop_dist_rads) < target_rads)))
    {
//      Serial.print("slow\t");
      // First check if we are coming to a stop
      if((pow(current_velocity, 2) - 2 * max_accel * step_size_rads) < 0)
      {
        // See if we should turn round
        if(current_step_count > step_target)
        {
          next_step_us = (2 * next_step_us) - last_step_us;
          set_dir(false);
        }
        else if(current_step_count < step_target)
        {
          next_step_us = (2 * next_step_us) - last_step_us;
          set_dir(true);
        }
        else
        {
          next_step_us = 4294967294;
          diff_exact_us = 4294967294;
        }
      }

      // Otherwise just decelerate normally
      else
      {
        double t0, t1;
        quad_solve(t0, t1, -max_accel, current_velocity, step_size_rads);
//        Serial.print("\t t0: ");
//        Serial.print(1000000 * t0);
//        Serial.print("\t t1: ");
//        Serial.print(1000000 * t1);
        double next_step_temp = 1000000 * min(t0, t1);
        diff_exact_us = next_step_temp;
        next_step_us = (uint32_t) (next_step_temp + 0.5);
        next_step_us += cur_step_us;
//        Serial.print("\t");
//        Serial.print(next_step_us);
      }
    }

    // Otherwise check if we can speed up
    else if(abs(current_velocity) < max_vel)
    {
//      Serial.print("speed\t");
      // Quadratic has 2 roots, only use one that results in positive time
      double t0, t1;
      quad_solve(t0, t1, max_accel, current_velocity, step_size_rads);
//      Serial.print("\t t0: ");
//      Serial.print(1000000 * t0);
//      Serial.print("\t t1: ");
//      Serial.print(1000000 * t1);
      double next_step_temp = 1000000 * max(t0, t1);
      diff_exact_us = next_step_temp;
      next_step_us = (uint32_t) (next_step_temp + 0.5);
      next_step_us += cur_step_us;
//      Serial.print("\t");
//      Serial.print(next_step_us);
    }

    // Last resort is maintain max speed
    else
    {
      next_step_us += 1000000 * step_size_rads / max_vel;
    }

    // Update current motor velocity
    current_velocity = step_size_rads * 1000000;
    current_velocity /= diff_exact_us;
    current_velocity = current_dir ? current_velocity : -current_velocity;
    current_velocity = abs(current_velocity) < 0.01 ? 0 : current_velocity;
    last_step_us = cur_step_us;

//    Serial.print("\t");
//    Serial.print(current_velocity);
//    Serial.println();
  }
  return true;
}

// Public - Return current position in rads
double stepper::get_current_rads()
{
  return 2 * PI * current_step_count / steps_per_rev;
}

// Private - Set stepper direction pin
void stepper::set_dir(bool dir)
{
  if(dir && !current_dir)
  {
    if(reverse)
      digitalWrite(dir_pin, LOW);
    else
      digitalWrite(dir_pin, HIGH);
    current_dir = true;
  }
  else if(!dir && current_dir)
  {
    if(reverse)
      digitalWrite(dir_pin, HIGH);
    else
      digitalWrite(dir_pin, LOW);
    current_dir = false;
  }
}

// Private - Take single step and update step count if control loop designates to do so
void stepper::take_step()
{
  digitalWrite(step_pin, HIGH);
  delayMicroseconds(1);
  digitalWrite(step_pin, LOW);
  if(current_dir) current_step_count++;
  else current_step_count--;
}

// Private - Quadratic equation yo
void stepper::quad_solve(double &t_0, double &t_1, double a, double b, double c)
{
  double temp0 = -abs(b);
  double temp1 = sqrt(pow(b, 2) + 2 * a * c);
  t_0 = (temp0 + temp1) / a;
  t_1 = (temp0 - temp1) / a;
}


/* GCODE PARSER STUFF */

gcode_command_floats::gcode_command_floats(vector<string> inputs)
{
  if (inputs.size() == 1)
    return;

  for(uint16_t arg_i = 1; arg_i < inputs.size(); arg_i++)
  {
    char char_value = '\0';
    float float_value = NOVALUE;
    parse_float(inputs[arg_i], char_value, float_value);

    commands.push_back(tolower(char_value));
    values.push_back(float_value);
  }
}

float gcode_command_floats::fetch(char com_key)
{
  vector<char>::iterator itr = find(commands.begin(), commands.end(), com_key);
  if (itr != commands.cend())
  {
    return values[distance(commands.begin(), itr)];
  }

  return NOVALUE;
}

bool gcode_command_floats::com_exists(char com_key)
{
  vector<char>::iterator itr = find(commands.begin(), commands.end(), com_key);
  if (itr != commands.cend())
  {
    return true;
  }

  return false;
}

void gcode_command_floats::parse_float(string inpt, char &cmd, float &value)
{
  if (inpt.length() > 0)
  {
    cmd = inpt[0];
    if (inpt.length() == 1)
      return;

    string temp_arg_char = "";
    for (uint32_t i = 1; i < inpt.length(); i++)
    {
      temp_arg_char += inpt[i];
    }
  
    value = stof(temp_arg_char);
  }
}
