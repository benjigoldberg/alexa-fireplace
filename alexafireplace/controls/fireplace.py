"""Controls for the fireplace"""

from datetime import datetime

import RPi.GPIO as GPIO

# Use the Pinout definitions rather than naive board pin count
GPIO.setmode(GPIO.BCM)

BLOWER_FAN = 23
#FIREPLACE = 
RF_RECEIVE = 19
RF_TRANSMIT = 6

# Initialize the Blower Fan Pin as Output
GPIO.setup([BLOWER_FAN, RF_TRANSMIT], GPIO.OUT)
GPIO.setup([RF_RECEIVE], GPIO.IN)


def get_blower_fan_state():
    """Returns the ``True`` if the blower fan is on, else ``False``"""
    return GPIO.input(BLOWER_FAN) == 1


def set_blower_fan(enable):
    """If `enable` is ``True``, turn on the blower fan, else turn it off."""
    signal = GPIO.HIGH if enable is True else GPIO.LOW
    GPIO.output(BLOWER_FAN, signal)


def get_flame_state():
    """Returns the ``True`` if the flame is on, else ``False``"""
    return False


def set_flame(enable):
    """If `enable` is ``True``, turn on the flame, else turn it off."""
    signal = GPIO.HIGH if enable is True else GPIO.LOW
    #GPIO.output(FIREPLACE, signal)

def record_remote_code():
    """Records a remote code"""
    cumulative_time = 0
    start = datetime.utcnow()
    times = []
    signals = []
    while cumulative_time < 5:
        timedelta = datetime.utcnow() - start
        times.append(timedelta)
        signals.append(GPIO.input(RF_RECEIVE))
        cumulative_time = timedelta.seconds
    for idx in range(len(times)):
        times[idx] = times[idx].seconds + times[idx].microseconds/1000000.
    return times, signals

