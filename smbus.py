from typehints import *

def smbus(
    scl : Pin,
    sda : Pin
) -> SMBus:
    def r():
        pass
    return r

def send_byte(smbus : SMBus, byte: int):
    pass

def send_bytes(smbus : SMBus, bytes : list[int]) -> None:
    if bytes:
        send_byte(smbus, bytes[0])
        send_bytes(smbus, bytes[1:])