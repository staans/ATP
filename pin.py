# returns a function that can be called to read or write to a pin using the read and write function provided
def pin(
    write_func: callable[[bool], None],
    read_func:  callable[[],     bool]
) -> callable[[bool], bool]:
    def r(val=None : bool | None) -> bool:
        if (val != None):
            write_func(val)
        return read_func()
    return r

# returns a function whose read and write functions interact with the simulation
def simulated_pin(
    pin_num: int
) -> callable[[bool], bool]:
    return pin(
        lambda h: None,
        lambda: False
    )