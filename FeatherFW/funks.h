#include <Adafruit_NeoPixel.h>
#include <Servo.h>
#include <string>
#include <vector>
#include <algorithm>

#define MAX_MSG_LEN 100
#define NOVALUE 999999

using namespace std;

/* RANDOMIO FUNCS */
void setLEDColor(int r, int g, int b);
void error_blink(uint8_t errcode);

/* SERIAL FUNCS */
void clear_data(char (&serial_data) [MAX_MSG_LEN]);
bool respondToSerial(char (&serial_data) [MAX_MSG_LEN]);

/* PARSING FUNCS */
void parse_inputs(char serial_data[MAX_MSG_LEN], vector<string> &args);
void parse_int(string inpt, char &cmd, int32_t &value);

/* DEBUG FUNCS */
void debug_print_str(string str);
