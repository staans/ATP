import ctypes
import pathlib

# some things should probably be different if i want it to work on windows, but i dont B-)

from simulation import Simulation

def init(sim : Simulation):
    libname = pathlib.Path().absolute() / "python/cpp_lib.so"
    lib = ctypes.CDLL(libname)

    SET_PIN_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_bool)
    set_pin_func = SET_PIN_FUNC(lambda pin, val : sim.digital_write(pin, val))

    READ_PIN_FUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_int)
    read_pin_func = READ_PIN_FUNC(lambda pin : sim.digital_read(pin))

    PIN_MODE_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p)
    pin_mode_func = PIN_MODE_FUNC(lambda pin, mode : sim.pin_mode(pin, mode.decode()))

    US_FUNC = ctypes.CFUNCTYPE(ctypes.c_ulong)
    us_func = US_FUNC(lambda: sim.time)

    DELAY_US_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_ulong)
    delay_us_func = DELAY_US_FUNC(lambda t: sim.sleep(t))

    init.funcs = (set_pin_func, read_pin_func, pin_mode_func, us_func, delay_us_func)

    lib.provide_set_pin_func(set_pin_func)
    lib.provide_read_pin_func(read_pin_func)
    lib.provide_pin_mode_func(pin_mode_func)
    lib.provide_us_func(us_func)
    lib.provide_delay_us_func(delay_us_func)

    lib.read_temperature.restype = ctypes.c_float
    lib.read_humidity.restype = ctypes.c_float

    return (lib.read_temperature, lib.read_humidity)