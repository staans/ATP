#!/usr/bin/env python3

def light_sensor(
    scl: callable[[bool|None], bool],
    sda: callable[[bool|None], bool]
) -> callable[[], float]:
    def r() -> float:
        # todo: actually read sensor with scl & sda
        return 0
    return r