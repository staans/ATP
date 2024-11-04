#include "python-binding.hpp"
#include "DHT.h"

void(*set_pin_func)(int, bool) = nullptr;
void set_set_pin_func(void(*func)(int, bool)) {
    set_pin_func = func;
}

bool(*read_pin_func)(int) = nullptr;
void set_read_pin_func(bool(*func)(int)) {
    read_pin_func = func;
}

unsigned long(*us_func)() = nullptr;
void set_us_func(unsigned long(*func)()) {
    us_func = func;
}

// makes pin high when setting mode to INPUT, since that should make connected wire floating (in some circumstances), and in my case my wires are pull-up
// is kinda a botch, but
void pinMode(int pin, PinMode mode) {

}


void digitalWrite(int pin, PinValue val) {

}

unsigned long millis() {
    return 1;
}

void delay(unsigned long ms) {

}

void delayMicroseconds(unsigned int us) {

}

// interupts don't exist in simulation, so uueeeh
void interrupts() {}
void noInterrupts() {}

PinValue digitalRead(int pin) {
    return HIGH;
}

float read_temperature() {
    return DHT(8, DHT22).readTemperature();
}

float read_humidity() {
    return DHT(8, DHT22).readHumidity();
}