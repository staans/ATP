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
    def read(self):
        r = self.reada()
        return r

    def reada(self) -> bool:
        # kinda badly written, but it doesn't really matter
        out_values = [pin.is_high for pin in self.pins if pin.is_output]
        
        # if wire isn't activiely being set by output pins
        if not out_values:
            # return high if any pins are pull up
            if any(pin.is_high for pin in self.pins):
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

        pullup = Pin()
        pullup.mode("INPUT_PULLUP")
        self.dht22 = DHT22(Wire([self.pins[8], pullup]))
        self.tsl2561 = TSL2561()

    # somewhat (i assume HIGH=1/true, LOW=0/false, which i cant figure out whether or not this is guaranteed in the arduino documentation) equivalent to digitalWrite in arduino
    def digital_write(self, pin_nr : int, value : bool) -> None:
        self.pins[pin_nr].write(value)
    
    # equivalent-ish (mode is a string instead of an enum) to pinMode in arduino
    def pin_mode(self, pin_nr : int, mode : str):
        self.pins[pin_nr].mode(mode)

    # equivalent to pinRead in arduino
    def digital_read(self, pin_nr : int) -> bool:
        r = self.pins[pin_nr].read()
        return r

    def sleep(self, time : Microseconds) -> None:
        self.time += time

        self.dht22.update(time)


class DHT22:
    def __init__(self, wire : Wire):
        # connections
        self.pin : Pin = Pin()
        wire.connect_to(self.pin)

        # state
        self.pin.mode('INPUT_PULLUP')
        self.state : str = 'start-pulse'
        self.state_progress = 0

        # signal creation
        self.temp : Celcius = 2.05
        self.humidity : float = 20.5
        self.signal : tuple[bool]

    # updates the state of the dht22
    # should be called every time the simulation progresses in time
    def update(self, delta_time : Microseconds):
        # could (maybe should) be rewritten to use a loop instead of recursion, but this works for now
        match self.state:
            # wait for a at least 1ms low as a start pulse
            case 'start-pulse':
                if self.pin.read() == False:
                    self.state_progress += delta_time
                else:
                    self.state_progress = 0

                if self.state_progress >= 1000:
                    overflow = self.state_progress - 1000
                    self.state_progress = 0
                    self.state = 'start-pause'
                    self.update(overflow)

            # wait for a 20-40us high after start pulse
            case 'start-pause':
                if self.pin.read() == True:
                    self.state_progress += delta_time
                else:
                    self.state_progress = 0

                if self.state_progress >= 30:
                    overflow = self.state_progress - 30
                    self.pin.mode('OUTPUT')
                    self.signal = self.get_signal()
                    self.state_progress = 0
                    self.state = 'sending'
                    self.update(overflow)

            case 'sending':
                self.state_progress += delta_time
                
                if self.state_progress < len(self.signal):
                    self.pin.write(self.signal[self.state_progress])
                else:
                    overflow = self.state_progress - len(self.signal)
                    self.pin.mode('INPUT')
                    self.state_progress = 0
                    self.state = 'start-pulse'
                    self.update(overflow)

    # returns a tuple describing the sequencing of raising and lowering the data pin
    def get_signal(self) -> tuple[bool]:
        signal : list[bool] = []

        # response signal + pause
        signal += [False] * 80 + [True] * 80

        temp_int = round(self.temp*10)
        temp_int_bin = bin(temp_int).removeprefix('-').removeprefix('0b').rjust(16, '0')
        temp_bin = ('1' if self.temp < 0 else '0') + temp_int_bin[1:]

        humid_int = round(self.humidity*10)
        humid_bin = bin(humid_int).removeprefix('-').removeprefix('0b').rjust(16, '0')

        check_bin = bin(int(humid_bin[:8], 2) + int(humid_bin[8:], 2) + int(temp_bin[:8], 2) + int(temp_bin[8:], 2)).removeprefix('0b')[-8:].rjust(8, '0')

        # # bits = 16 bits unsigned humidity in either percentage or just normal idk, 16 bits signed temperature in deci-celius, 8 bit check-sum

        bits = humid_bin + temp_bin + check_bin

        # bits to signals
        for bit in bits:
            signal.extend([False]*50)
            if bit == '1':
                signal.extend([True]*70)
            elif bit == '0':
                signal.extend([True]*26)
        signal.extend([False]*50)

        return tuple(signal)

class TSL2561:
    pass

