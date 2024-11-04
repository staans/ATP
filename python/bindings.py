import ctypes
import pathlib

# some things should probably be different if i want it to work on windows, but i dont B-)

from simulation import Simulation

def init(sim : Simulation):
    libname = pathlib.Path().absolute() / "python/cpp_lib.so"
    lib = ctypes.CDLL(libname)

    SET_PIN_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_bool);
    set_pin_func = lambda pin, val : sim.set_pin(pin, val)

    lib.set_set_pin_func(SET_PIN_FUNC(set_pin_func))

    lib.read_temperature.restype = ctypes.c_float;
    def read_temp():
        lib.read_temperature()

    return read_temp;