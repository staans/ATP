from typehints import *

# the only stateful code in this project B-)

class Simulation:
    def __init__(self):
        self.pins : list[bool] = [False] * 32
        self.time : Microseconds = 0
        self.dht22 = DHT22()
        self.tsl2561 = TSL2561()

    def update(self) -> None:
        pass

    def set_pin(self, pin_nr : int, value : False) -> None:
        self.pins[pin_nr] = value
    
    def sleep(self, time : Microseconds) -> None:
        self.time += time


class DHT22:
    def __init__(self, pin : int):
        self.pin : int = pin
        self.state : str = 'stand-by'

    # updates the state of the dht22 and returns the value it wants to set to its data-pin
    # should be called every time the simulation progresses in time
    # doesnt nececcarrilliyu work with pulses split between calls, eg, calling this function once != calling it twice with same pins and halved delta-time
    def get_output(self, deltatime : Microseconds, pins : tuple[bool]) -> bool:

        match self.state:
            # wait for a start pulse from mcu of at least 1ms
            case 'start-pulse':
                if deltatime >= 1000 and not pins[self.pin]:
                    state = 'start-pause'
                return pins[self.pin]

            # wait 20-40us after start pulse
            case 'start-pause':
                if deltatime >= 30 and pins[self.pin]:
                    state = 'presence-pulse'
                return pins[self.pin]

            # return a pulse after start pulse and waiting
            case 'presence-pulse':
                pass

            case 'presence-pause':
                pass

            case 'bit-signal':
                pass

            case 'bit-zero-pause':
                pass

            case 'bit-one-pause':
                pass

    # returns a tuple describing the sequencing of raising and lowering the data pin
    def get_signal(self, temp : Celcius, humid : float) -> tuple[bool]:
        signal : list[bool]

        # response signal + pause
        signal += [False] * 80 + [True] * 80

        # convert units to bits
        humid_int = int(humid)
        humid_int_bin = bin(humid_int)[2:].ljust(8, '0')
        humid_decimal = humid % 1
        humid_decimal_bin = bin(int(humid_decimal*256))[2:].ljust(8, '0')
        humid_bin = humid_int_bin + humid_decimal_bin

        temp_int = int(temp)
        temp_int_bin = bin(temp_int)[2:].ljust(8, '0')
        temp_decimal = temp % 1
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

