#include "python-binding.hpp"
#include "DHT.h"

#define ja true
#define nee false

void(*set_pin_func)(int, bool) = nullptr;
extern "C" void set_set_pin_func(void(*func)(int, bool)) {
    set_pin_func = func;
}

bool(*read_pin_func)(int) = nullptr;
extern "C" void set_read_pin_func(bool(*func)(int)) {
    read_pin_func = func;
}

unsigned long(*us_func)(void) = nullptr;
extern "C" void set_us_func(unsigned long(*func)(void)) {
    us_func = func;
}

void(*delay_us_func)(unsigned long) = nullptr;
extern "C" void set_delay_us_func(void(*func)(unsigned long)) {
    delay_us_func = func;
}

// makes pin high when setting mode to INPUT, since that should make connected wire floating (in some circumstances), and in my case my wires are pull-up
// is kinda a botch, but
void pinMode(int pin, PinMode mode) {
    if (mode == INPUT)
        digitalWrite(pin, HIGH);
}

void digitalWrite(int pin, PinValue val) {
    set_pin_func(pin, val == HIGH);
}

unsigned long millis() {
    return us_func() / 1000;
}

void delay(unsigned long ms) {
    delay_us_func(ms*1000);
}

void delayMicroseconds(unsigned int us) {
    delay_us_func(us);
}

// interupts don't exist in simulation, so uueeeh
void interrupts() {}
void noInterrupts() {}

PinValue digitalRead(int pin) {
    return HIGH;
}

extern "C" float read_temperature() {
    return DHT(8, DHT22).readTemperature();
}

extern "C" float read_humidity() {
    return DHT(8, DHT22).readHumidity();
}