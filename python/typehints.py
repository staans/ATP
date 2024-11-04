from collections.abc import Callable
from dataclasses import dataclass

# 'types.py' is actually a better name for this file but that's already used by pythons standard libarary B-(

# a pin is a function that takes an optional boolean argument.
# If the bool is provided, it sets the pin to the value and returns it. If it isn't given, it reads the pin and returns that.
type Pin = Callable[[bool|None], bool]

type SMBus = int

# relevant units
type LitersPerSecond = float
type Celcius = float
type Lux = float
type Microseconds = int

# a pump is a function which takes a liters per second, and sets the pump's flowrate to that amount
type Pump = Callable[[LitersPerSecond], None]

# a reading from the temperature/humidity sensor
# relative humidity is an unitless ratio
@dataclass
class TempHumidReading:
    temperature: Celcius
    humidity: float

# a temp/humidity sensor is a function that takes no arguments and returns the measured TempHumidReading
type TempHumidSensor = Callable[[], TempHumidReading]

# A lightsensor is a function which takes no arguments and returns the measured amount of light
type LightSensor = Callable[[], Lux]