import pyvisa
import time
import atexit
from time import sleep, strftime, localtime
from datetime import timedelta
import csv
import os
import threading
import RPi.GPIO as GPIO
import smbus
from pyvisa.constants import StopBits, Parity


def setup():
        rm=pyvisa.ResourceManager()
        resources = rm.list_resources()
        print(resources)
        print(rm)
        if resources == None:
            print("No connected devices found")
    
        DMM = rm.open_resource(resources[0],
            baud_rate=9600, data_bits=8, flow_control=4,
            parity = Parity.none,stop_bits=StopBits.two)
        DMM.write("SYST:REM")
        sleep(1)
        #clear buffers
       
        #set read/write terminators to dictate end of command"
        DMM.read_termination = '\n'
        DMM.write_termination = '\n'
        DMM.write("*rst; status:preset; *cls")
        #Enable remote mode to interface with multimeter
        sleep(1)
        DMM.write("*IDN?")
       
        sleep(1)
        print("Connection Established with " + DMM.read())
        return DMM