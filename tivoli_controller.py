#!usr/bin/env python

import dbus
import CHIP_IO.GPIO as GPIO

# Defines
aux_pin = 'XIO-P0'
audio_connect_pin = 'XIO-P1'

shairport = 'shairport_sync.service'
spotify_connect = 'spotify_connect_web.service'

if __name__ == '__main__':

    # Set up the SystemD stuff
    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/opt/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
    
    # Set up the pins
    GPIO.setup(aux_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(audio_connect_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    was_enabled = False
    
    while True:
        enable = not (GPIO.input(aux_pin) and GPIO.input(audio_connect_pin))
        
        if enable and not was_enabled:
            job = manager.StartUnit(shairport, 'fail')
            job = manager.StartUnit(spotify_connect, 'fail')
        else if not enable and was_enabled:
            job = manager.StopUnit(shairport, 'fail')
            job = manager.StopUnit(spotify_connect, 'fail')
        
        was_enabled = enable
        
        sleep(0.2)

