from typehints import Microseconds

# the only stateful code in this project B-)

# class representing a pin. write, mode and read corrospond to digitalWrite, pinMode and digitalRead in arduino
# must be connected to a wire before reading by doing Wire(pins) or wire.connect_to(pin)
class Pin:
    def __init__(self):
        self.is_output = False
        # is_high is also used when the pin is input to decide if the internal pull-up resistor is used (an actual arduino also uses the same value for both)
        self.is_high = False
        self.wire = None

    def write(self, value : False) -> None:
        self.is_high = value

    # set mode of the pin. mode can be 'INPUT', 'INPUT_PULLUP' or 'OUTPUT'.
    def mode(self, mode : str):
        if mode == 'INPUT':
            self.is_output = False
            self.is_high = False # this line only correctly emulated arduino after v1.0.1 released in 2012. It seems to be fine with my code c++ code though
        elif mode == 'INPUT_PULLUP':
            self.is_output = False
            self.is_high = True
        elif mode == 'OUTPUT':
            self.is_output = True
        else:
            raise Exception("Du bist ein stupide")

    # reads and returns value of associated wire. raises if mode is output or if not connected to a wire or if floating or if short circuit
    def read(self) -> bool:
        if self.is_output:
            raise Exception("urgh argh me no garg")

        if not self.wire:
            raise Exception("me when no wire")
            
        return self.wire.read()

# class representing pins connected together. ground connection isn't modelled
class Wire:
    def __init__(self, pins : list[Pin]):
        self.pins = pins
        for pin in self.pins:
            pin.wire = self
    
    # add another pin
    def connect_to(self, pin : Pin):
        self.pins.append(pin)
        pin.wire = self

    # returns true if high, false if low. raises exceptions if floating or short circuit
    def read(self) -> bool:
        # kinda badly written, but it doesn't really matter
        out_values = [pin.is_high for pin in self.pins if pin.is_output]
        
        # if wire isn't activiely being set by output pins
        if not out_values:
            # return high if a pull up
            if [pin.is_high for pin in self.pins if not pin.is_output]:
                return True
            # raise if otherwise (is floating)
            raise Exception("uh oh, ik haat drijven")
        
        # return high if all output pins are high
        if all(out_values):
            return True
        # return low if all output pins are low
        if not any(out_values):
            return False
        
        # if there are out_values but some are high and some are low, then there is a short circuit
        # raise an error and a stink
        raise Exception("me when ")
    

class Simulation:
    def __init__(self):
        # arduino and simulation thingies
        self.pins : list[Pin] = [Pin() for i in range(32)]
        self.time : Microseconds = 0

        self.dht22 = DHT22(Wire([self.pins[8]]))
        self.tsl2561 = TSL2561()

    # somewhat (i assume HIGH=1/true, LOW=0/false, which i cant figure out whether or not this is guaranteed in the arduino documentation) equivalent to digitalWrite in arduino
    def digital_write(self, pin_nr : int, value : bool) -> None:
        self.pins[pin_nr].write(value)
    
    # equivalent-ish (mode is a string instead of an enum) to pinMode in arduino
    def pin_mode(self, pin_nr : int, mode : str):
        print(pin_nr, mode)
        self.pins[pin_nr].mode(mode)

    # equivalent to pinRead in arduino
    def digital_read(self, pin_nr : int) -> bool:
        print(pin_nr, self.pins[pin_nr].read())
        return self.pins[pin_nr].read()

    def sleep(self, time : Microseconds) -> None:
        self.dht22.update(time)
        self.time += time


class DHT22:
    def __init__(self, wire : Wire):
        self.pin : Pin = Pin()
        wire.connect_to(self.pin)
        self.state : str = 'start-pulse'
        self.temp : Celcius = 21
        self.humidity : float = .9
        self.send_progress : Microseconds
        self.signal : tuple[bool]

    # updates the state of the dht22
    # should be called every time the simulation progresses in time
    def update(self, delta_time : Microseconds):
        print(self.state)
        match self.state:
            # wait for a start pulse from mcu of at least 1ms
            case 'start-pulse':
                if delta_time >= 1000 and self.pin.read() == False:
                    self.state = 'start-pause'
                return

            # wait 20-40us after start pulse
            case 'start-pause':
                if delta_time >= 30:
                    self.send_progress = 0
                    self.signal = self.get_signal()
                    self.pin.mode('OUTPUT')
                    self.state = 'sending'
                return

            # send signals. currently has some thingies that could go wrong if the pulse length for 'start-pause' is too long, due to it consuming all of time
            case 'sending':
                self.send_progress += delta_time
                signal = self.get_signal()
                if self.send_progress >= len(signal):
                    self.state = 'start-pulse'
                    self.pin.mode('INPUT')
                self.pin.write(self.signal[self.send_progress])
                return

    # returns a tuple describing the sequencing of raising and lowering the data pin
    def get_signal(self) -> tuple[bool]:
        signal : list[bool] = []

        # response signal + pause
        signal += [False] * 80 + [True] * 80

        # convert units to bits
        humid_int = int(self.humidity)
        humid_int_bin = bin(humid_int)[2:].ljust(8, '0')
        humid_decimal = self.humidity % 1
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

