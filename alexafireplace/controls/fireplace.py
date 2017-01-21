"""Controls for the fireplace"""

import RPi.GPIO as GPIO

# Use the Pinout definitions rather than naive board pin count
GPIO.setmode(GPIO.BCM)

BLOWER_FAN = 23
#FIREPLACE = 

# Initialize the Blower Fan Pin as Output
GPIO.setup([BLOWER_FAN], GPIO.OUT)


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

