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
        self.pin = pin
        self.state = 'stand-by'

    # updates the state of the dht22 and returns the value it wants to set to its data-pin
    # should be called every time the simulation progresses in time
    def get_output(self, time : Microseconds, pins : tuple[bool]) -> bool:
        match self.state:
            case 'stand-by':
                pass
            case 'start-pulse':
                pass
            case 'start-pause':
                pass
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


class TSL2561:
    pass

