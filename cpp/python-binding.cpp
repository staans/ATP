#include "python-binding.hpp"
#include "DHT.h"

void(*set_pin_func)(int, bool) = nullptr;
extern "C" void provide_set_pin_func(void(*func)(int, bool)) {
    set_pin_func = func;
}

bool(*read_pin_func)(int) = nullptr;
extern "C" void provide_read_pin_func(bool(*func)(int)) {
    read_pin_func = func;
}

void(*pin_mode_func)(int, char*) = nullptr;
extern "C" void provide_pin_mode_func(void(*func)(int, char*)) {
    pin_mode_func = func;
}

unsigned long(*us_func)(void) = nullptr;
extern "C" void provide_us_func(unsigned long(*func)()) {
    us_func = func;
}

void(*delay_us_func)(unsigned long) = nullptr;
extern "C" void provide_delay_us_func(void(*func)(unsigned long)) {
    delay_us_func = func;
}


void pinMode(int pin, PinMode mode) {
    switch (mode) {
        case PinMode::INPUT:
            pin_mode_func(pin, (char*)"INPUT\0");
            return;
        case PinMode::INPUT_PULLUP:
            pin_mode_func(pin, (char*)"INPUT_PULLUP\0");
            return;
        case PinMode::OUTPUT:
            pin_mode_func(pin, (char*)"OUTPUT\0");
            return;
    }
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
    return read_pin_func(pin) ? HIGH : LOW;
}

extern "C" float read_temperature() {
    auto dht = DHT(8, DHT22, 60);
    dht.begin();
    return dht.readTemperature();
}

extern "C" float read_humidity() {
    auto dht = DHT(8, DHT22, 60); // why is the default amount of microseconds to differnciatate zeros and ones 6 us? very much seems like a typo but idk
    dht.begin();
    return dht.readHumidity();
}