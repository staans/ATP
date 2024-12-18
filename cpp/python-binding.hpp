#pragma once

#include <cstdint>
#include <cmath>

typedef bool boolean;

enum PinMode {
    INPUT,
    OUTPUT
};

enum PinValue {
    HIGH,
    LOW
};

extern void(*set_pin_func)(int, bool);
extern bool(*read_pin_func)(int);
extern unsigned long(*us_func)();
extern void(*delay_us_func)(unsigned long);

extern "C" void set_set_pin_func(void(*func)(int, bool));
extern "C" void set_read_pin_func(bool(*func)(int));
extern "C" void set_us_func(unsigned long(*func)());
extern "C" void set_delay_us_func(void(*func)(unsigned long));

void pinMode(int pin, PinMode mode);
void digitalWrite(int pin, PinValue val);

unsigned long millis();
void delay(unsigned long ms);
void delayMicroseconds(unsigned int us);

void interrupts();
void noInterrupts();

PinValue digitalRead(int pin);

extern "C" float read_temperature();
extern "C" float read_humidity();