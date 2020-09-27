// Read serial messages if exist
bool respondToSerial(char (&serial_data) [MAX_MSG_LEN])
{
  uint8_t index = 0;
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      char newchar = Serial.read();
      if ((newchar != '\n') and (index < MAX_MSG_LEN)) {
        serial_data[index] = newchar;
        index++;
      }
      else {
        break;
      }
    }
    return true;
  }
  return false;
}

void clear_data(char (&serial_data) [MAX_MSG_LEN]) {
  for (uint16_t i = 0; i < MAX_MSG_LEN; i++) {
    serial_data[i] = '\0';
  }
}

void setLEDColor(int r, int g, int b)
{
  pixel.setPixelColor(0, pixel.Color(r, g, b)); // Set LED to red
  pixel.show();
}

void parse_inputs(char serial_data[MAX_MSG_LEN], vector<string> &args) {
  char delim = ' ';
  uint32_t index = 0;
  string temp_arg_str = "";

  while (serial_data[index] != '\0') {
    temp_arg_str += serial_data[index];
    index++;
    if (serial_data[index] == delim) {
      args.push_back(temp_arg_str);
      temp_arg_str = "";
      index++;
    }

    // timeout
    if (index > MAX_MSG_LEN) return;
  }
  args.push_back(temp_arg_str);
}

void debug_print_str(string str)
{
  for (uint16_t i = 0; i < str.length(); i++)
  {
    Serial.print(str[i]);
  }
  Serial.println();
}

void parse_int(string inpt, char &cmd, int32_t &value)
{
  cmd = '\0';
  value = NOVALUE;
  cmd = inpt[0];
  string temp_arg_char = "";
  for (uint32_t i = 1; i < inpt.length(); i++)
  {
    temp_arg_char += inpt[i];
  }

  value = stoi(temp_arg_char);
}

void error_blink(uint8_t errcode)
{
  while (true)
  {
    for(uint8_t i = 0; i < errcode; i++)
    {
      setLEDColor(200, 0, 0);
      delay(50);
      setLEDColor(0, 0, 0);
      delay(150);
    }
    delay(500);
  }
}
