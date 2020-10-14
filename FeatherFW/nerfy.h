#include "funks.h"
#include "pins.h"

Adafruit_NeoPixel pixel = Adafruit_NeoPixel(1, 8, NEO_GRB + NEO_KHZ800);

using namespace std;

struct stepper
{
  stepper(int s_pin, int d_pin, int e_pin, bool rev);

  public:
  void enable();
  void disable();
  void update_config(int32_t steps_per_rev_new, float max_vel_new, float max_accel_new);
  void set_current_rads(double rads);
  void set_rad_target(double target, float feedrate);
  bool step_if_needed();
  double get_current_rads();
  double get_current_vel();

  private:
  // Configuration
  int step_pin;
  int dir_pin;
  int en_pin;
  bool reverse;
  float steps_per_rev = 3200;
  float max_vel = 5;
  float max_accel = 5;
  float step_size_rads = 2 * PI / 3200;

  // Backend funcs
  void set_dir(bool dir);
  void take_step();
  void quad_solve(double &t_0, double &t_1, double a, double b, double c);

  // Control vars
  double target_rads = 0;

  // Motion tracking vars
  bool current_dir = false;
  double current_velocity = 0;
  int32_t current_step_count = 0;
  double diff_exact_us = 0;
  uint32_t last_step_us = 0;
  uint32_t next_step_us = 0;
};

struct gcode_command_floats
{
  gcode_command_floats(vector<string> inputs);

  public:
  float fetch(char com_key);
  bool com_exists(char com_key);
  

  private:
  void parse_float(string inpt, char &cmd, float &value);

  vector<char> commands;
  vector<float> values;
};
