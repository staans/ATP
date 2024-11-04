#!/usr/bin/env python3

from collections.abc import Callable

def light_sensor(

) -> Callable[[], float]:
    def r() -> float:
        # todo: actually read sensor with scl & sda
        return 0
    return r