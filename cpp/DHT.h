#ifndef DHT_H
#define DHT_H

#define PYTHON 1

#if ARDUINO >= 100
 #include "Arduino.h"
#elif PYTHON
 #include "python-binding.hpp"
#else
 #include "WProgram.h"
#endif


/* DHT library 

MIT license
written by Adafruit Industries
*/

// i forgot where i actually got this library from but it seems really outdated now that i take a closer look at it
// nevertheless, it seems to be working somewhat

// how many timing transitions we need to keep track of. 2 * number bits + extra
#define MAXTIMINGS 85

#define DHT11 11
#define DHT22 22
#define DHT21 21
#define AM2301 21

class DHT {
 private:
  uint8_t data[6];
  uint8_t _pin, _type, _count;
  unsigned long _lastreadtime;
  boolean firstreading;

 public:
  DHT(uint8_t pin, uint8_t type, uint8_t count=6);
  void begin(void);
  float readTemperature(bool S=false);
  float convertCtoF(float);
  float convertFtoC(float);
  float computeHeatIndex(float tempFahrenheit, float percentHumidity);
  float readHumidity(void);
  boolean read(void);

};
#endif