from typehints import *

# the only stateful code in this project B-)

class Simulation:
    def __init__(self):
        self.pins : list[bool] = [False] * 32
        self.time : Microseconds = 0
        self.dht22 = DHT22(8)
        self.tsl2561 = TSL2561()

    def set_pin(self, pin_nr : int, value : False) -> None:
        self.pins[pin_nr] = value
    
    def sleep(self, time : Microseconds) -> None:
        self.time += time

        self.dht22.get_output(self.time, tuple(self.pins))


class DHT22:
    def __init__(self, pin : int):
        self.pin : int = pin
        self.state : str = 'stand-by'
        self.temp : Celcius = 21
        self.humidity : float = .9
        self.send_progress : Microseconds
        self.signal : tuple[bool]

    # updates the state of the dht22 and returns what value it sets to pin (True = high, False = low. pin is open-collector thing and data wire is pulled-high)
    # should be called every time the simulation progresses in time
    # doesnt nececcarrilliyu work with pulses split between calls, eg, calling this function once != calling it twice with same pins and halved delta-time
    def get_output(self, delta_time : Microseconds, pins : tuple[bool]) -> bool:

        match self.state:
            # wait for a start pulse from mcu of at least 1ms
            case 'start-pulse':
                if delta_time >= 1000 and not pins[self.pin]:
                    state = 'start-pause'
                return True

            # wait 20-40us after start pulse
            case 'start-pause':
                if delta_time >= 30 and pins[self.pin]:
                    self.send_progress = 0
                    self.signal = self.get_signal()
                    state = 'sending'
                return True

            # send signals. currently has some thingies that could go wrong if the pulse length for 'start-pause' is too long, due to it consuming all of time
            case 'sending':
                self.send_progress += delta_time
                signal = self.get_signal()
                if self.send_progress >= len(signal):
                    self.state = 'start-pulse'
                    return pins[self.pin]
                return self.signal[send_progress]

    # returns a tuple describing the sequencing of raising and lowering the data pin
    def get_signal(self) -> tuple[bool]:
        signal : list[bool]

        # response signal + pause
        signal += [False] * 80 + [True] * 80

        # convert units to bits
        humid_int = int(humid.humid)
        humid_int_bin = bin(humid_int)[2:].ljust(8, '0')
        humid_decimal = humid.humid % 1
        humid_decimal_bin = bin(int(humid_decimal*256))[2:].ljust(8, '0')
        humid_bin = humid_int_bin + humid_decimal_bin

        temp_int = int(self.temp)
        temp_int_bin = bin(temp_int)[2:].ljust(8, '0')
        temp_decimal = self.temp % 1
        temp_decimal_bin = bin(int(temp_decimal*256))[2:].ljust(8, '0')
        temp_bin = temp_int_bin + temp_decimal_bin

        check_bin = bin(int(temp_int_bin, 2) + int(temp_decimal_bin, 2) + int(humid_int_bin, 2) + int(humid_decimal_bin, 2))[2:]
        
        bits = humid_int_bin + humid_decimal_bin + temp_int_bin + temp_decimal_bin + check_bin

        # bits to signals
        for bit in bits:
            signal.extend([False]*50)
            signal.extend([True]*(70 if bit=='1' else 26))

        return tuple(signal)


class TSL2561:
    pass

