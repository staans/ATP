from simulation import Simulation
from typehints import *

# returns a function that can be called to read or write to a pin using the read and write function provided
def pin(
    write_func : Callable[[bool], None],
    read_func :  Callable[[],     bool]
) -> Pin:
    def r(val : bool|None = None) -> bool:
        if (val != None):
            write_func(val)
        return read_func()
    return r

# returns a function whose read and write functions interact with the simulation
def simulated_pin(
    pin_num : int,
    sim : Simulation
) -> Pin:
    return pin(
        lambda v: sim.set_pin(pin_num, v),
        lambda: sim.pins[pin_num]
    )