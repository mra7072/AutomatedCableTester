
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
import json
from pyvisa import constants
import time
import serial
    #clear buffers




def setup():
        rm=pyvisa.ResourceManager()
        resources = rm.list_resources()
        
       # ASRL/dev/ttyS0::INSTR
        DMM = rm.open_resource('ASRL/dev/ttyS0::INSTR',
        baud_rate=9600, data_bits=8,
        parity = Parity.none,stop_bits=StopBits.one)
        print(DMM)
      
        
        DMM.read_termination = '\n'
        DMM.write_termination = '\n'
        DMM.write("*rst; status:preset; *cls")
        #Enable remote mode to interface with multimeter
        sleep(1)
        DMM.write("*IDN?")

        sleep(1)
        print("Connection Established with " + DMM.read())
        
        return DMM
        #print(DMM.write("*IDN?"))
       # DMM.write("SYST:REM")
      
        
def setup2():
        ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
        #ser.write("SYST:REM")
        ser.write("MEAS:RES?")
        
       # print(ser
        print(ser.readline())
        
        
        

        
        #DMM.write("*IDN?")
        #measureResistance(DMM)
        
        #DMM.write("MEAS:RES?")
        
        #DMM.write("SYST:REM")
       # DMM.write("DISP:FUCK")

        
      
    
def measureResistance(DMM):
    print("Initated measurement command")
    meas = DMM.query("MEAS:RES?")
    #res = DMM.query_ascii_values("MEAS:RES?")
    print("Measured resistance:" + str(res[0]) + " ohms")
    #clear buffer
    DMM.write("*rst; status:preset; *cls")
    return res        
        
    
if __name__ == '__main__':
       DMM = setup()
       #measureResistance(DMM)
       #DMM.write("MEAS:RES?")
       #sleep(1.47)
       #print(DMM.read())
       
       #res = DMM.query_ascii_values("MEAS:RES?")
       print(res[0])
     
       
    
       