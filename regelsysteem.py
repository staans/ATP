def regelsysteem(
    light_sensor: callable[[], float],
    temp_humid_sensor: callable[[], tuple[float, float]],
    warm_pump: callable[[float], None],
    cold_pump: callable[[float], None],
) -> None:
    # main loop
    while True:
        # todo: main loop logica
        # input-process-output loop
        pass