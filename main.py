#!/usr/bin/env python3
import logging
import time
import serial
from knikkersorteermachine import KnikkerSorteerMachine

with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0) as serial:
    machine = KnikkerSorteerMachine(serial, logging.DEBUG)

    chute_position = 0
    while True:
        machine.move_chute(chute_position)

        chute_position += 1
        if chute_position > 6:
            chute_position = 0

        time.sleep(0.2)

        machine.feed_one()

        time.sleep(1)
