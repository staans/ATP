#pragma once

#include <cstdint>
#include <cmath>

typedef bool boolean;

enum PinMode {
    INPUT,
    OUTPUT,
    INPUT_PULLUP
};

enum PinValue {
    LOW,
    HIGH,
};

extern void(*set_pin_func)(int, bool);
extern bool(*read_pin_func)(int);
extern void(*pin_mode_func)(int, char*);
extern unsigned long(*us_func)();
extern void(*delay_us_func)(unsigned long);

extern "C" void provide_set_pin_func(void(*func)(int, bool));
extern "C" void provide_read_pin_func(bool(*func)(int));
extern "C" void provide_pin_mode_func(void(*func)(int, char*));
extern "C" void provide_us_func(unsigned long(*func)());
extern "C" void provide_delay_us_func(void(*func)(unsigned long));

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