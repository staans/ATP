import ctypes
import pathlib

# some things should probably be different if i want it to work on windows, but i dont B-)

from simulation import Simulation

def init(sim : Simulation):
    libname = pathlib.Path().absolute() / "python/cpp_lib.so"
    lib = ctypes.CDLL(libname)

    SET_PIN_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_bool)
    set_pin_func = SET_PIN_FUNC(lambda pin, val : sim.set_pin(pin, val))

    READ_PIN_FUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_int)
    read_pin_func = READ_PIN_FUNC(lambda pin : sim.pins[pin])

    US_FUNC = ctypes.CFUNCTYPE(ctypes.c_ulong)
    us_func = US_FUNC(lambda: sim.time)

    DELAY_US_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_ulong)
    delay_us_func = DELAY_US_FUNC(lambda t: sim.sleep(t))

    init.funcs = (set_pin_func, read_pin_func, us_func, delay_us_func)

    lib.set_set_pin_func(set_pin_func)
    lib.set_read_pin_func(read_pin_func)
    lib.set_us_func(us_func)
    lib.set_delay_us_func(delay_us_func)

    lib.read_temperature.restype = ctypes.c_float
    def read_temp():
        return lib.read_temperature()

    return read_temp