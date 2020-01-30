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


"""
Creates a resource manager and performs proper connection to multimeter device.
Sets parameters
"""


def CreateTimer():
    return threading.Timer(2.0, "Timer created")

def StartTimer():
    return

def EndTimer():
    return

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

        

def runAutomatedTest(DMM):
    return measureResistance(DMM)



"""
Creates a new CSV file for the cable tested or update existing CSV and append new run
"""
def createNewCSV(serial, resistance):
    if(os.path.exists(serial + ".csv")):
        #just append to newline
        append_write = 'a'
    else:
        append_write = 'w'

    #create new file
    with open(serial + ".csv", append_write,newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #filewriter.writerow(['Cable Serial#', resistance])
        filewriter.writerow(['Cable Serial#','Test Run #' 'Measured Resistance', 'Expected Resistance', 'Time Elapsed, ''Pass/Fail'])



#TODO - Add validation checks against lookuptables
def ValidateData():
    return

#TODO - load lookuptables into memory
def loadLookUpTables():
    return



def DeterminePassFail():
    #Compare resistance to baseline
    return

def GPIO_SETUP(list_low,list_high):

   # GPIO.output(chan_list, GPIO.LOW) # all LOW
    GPIO.setmode(GPIO.BOARD) #selects by GPIO (e.g GPIO4)

    GPIO.setup(list_low, GPIO.OUT)

    GPIO.setup(list_high, GPIO.OUT)

    #precedence
    GPIO.output(list_low,GPIO.LOW)
    GPIO.output(list_high,GPIO.HIGH)

  #  loop through 50 times, on/off for 1 second

    #print(GPIO.input(4))

    #GPIO.cleanup()

def I2C_GPIO(D1_GPA_VAL_J6, D1_GPB_VAL_J6, D2_GPA_VAL_J6, D2_GPB_VAL_J6,D1_GPA_VAL_J7, D1_GPB_VAL_J7, D2_GPA_VAL_J7, D2_GPB_VAL_J7):
    bus = smbus.SMBus(1)
    DEVICE1 = 0x20 # Device address (A0-A2)
    DEVICE2 = 0x21

    # Pin direction register
    IODIRA = 0x00
    IODIRB = 0x01
    OLATA  = 0x14 # GPA
    OLATB  = 0x15 # GPB

   #setting to output mode
    bus.write_byte_data(DEVICE1,IODIRA,0x00)
    bus.write_byte_data(DEVICE1,IODIRB,0x00)
    bus.write_byte_data(DEVICE2,IODIRA,0x00)
    bus.write_byte_data(DEVICE2,IODIRB,0x00)

    D1_GPA_VAL = D1_GPA_VAL_J6 | D1_GPA_VAL_J7
    D1_GPB_VAL = D1_GPB_VAL_J6 | D1_GPB_VAL_J7
    D2_GPA_VAL = D2_GPA_VAL_J6 | D2_GPA_VAL_J7
    D2_GPB_VAL = D2_GPB_VAL_J6 | D2_GPB_VAL_J7

    bus.write_byte_data(DEVICE1,OLATA,D1_GPA_VAL)
    bus.write_byte_data(DEVICE1,OLATB,D1_GPB_VAL)

    bus.write_byte_data(DEVICE2,OLATA,D2_GPA_VAL)
    bus.write_byte_data(DEVICE2,OLATB,D2_GPB_VAL)


def I2C_GPIO(J6_LIST, J7_LIST):
    bus = smbus.SMBus(1)
    DEVICE1 = 0x20 # Device address (A0-A2)
    DEVICE2 = 0x21

    #print(J6_LIST)
    #print(J7_LIST)
    
    D1_GPA_VAL_J6 =   int(J6_LIST[0], 16)
    
    D1_GPB_VAL_J6 =   int(J6_LIST[1], 16)
    

    D2_GPA_VAL_J6 =   int(J6_LIST[2], 16)
    
        
    D2_GPB_VAL_J6 =   int(J6_LIST[3], 16)


    D1_GPA_VAL_J7 =   int(J7_LIST[0], 16)
    D1_GPB_VAL_J7 =   int(J7_LIST[1], 16)
    
    D2_GPA_VAL_J7 =   int(J7_LIST[2], 16)

    D2_GPB_VAL_J7 =   int(J7_LIST[3], 16)


    # Pin direction register
    IODIRA = 0x00
    IODIRB = 0x01

    OLATA  = 0x14 # GPA
    OLATB  = 0x15 # GPB

   #setting to output mode
    bus.write_byte_data(DEVICE1,IODIRA,0x00)
    bus.write_byte_data(DEVICE1,IODIRB,0x00)
    bus.write_byte_data(DEVICE2,IODIRA,0x00)
    bus.write_byte_data(DEVICE2,IODIRB,0x00)

    D1_GPA_VAL = D1_GPA_VAL_J6 | D1_GPA_VAL_J7
    D1_GPB_VAL = D1_GPB_VAL_J6 | D1_GPB_VAL_J7
    D2_GPA_VAL = D2_GPA_VAL_J6 | D2_GPA_VAL_J7
    D2_GPB_VAL = D2_GPB_VAL_J6 | D2_GPB_VAL_J7

    bus.write_byte_data(DEVICE1,OLATA,D1_GPA_VAL)
    bus.write_byte_data(DEVICE1,OLATB,D1_GPB_VAL)

    bus.write_byte_data(DEVICE2,OLATA,D2_GPA_VAL)
    bus.write_byte_data(DEVICE2,OLATB,D2_GPB_VAL)





def get_JSON_file():
    with open('9pin.json') as f:
      data = json.load(f)
      return data

  # for x in data:
  #     print(x["Name"])
def setup():
        rm=pyvisa.ResourceManager()
        resources = rm.list_resources()
        print(resources)
        print(rm)
        if resources == None:
            print("No connected devices found")

        DMM = rm.open_resource('ASRL/dev/ttyS0::INSTR',
        baud_rate=9600, data_bits=8,
        parity = Parity.none,stop_bits=StopBits.one)
       # DMM.write("SYST:REM")
       # sleep(1)
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
    


"""
Issues a measurement command, performs measurement, and returns measurement value
"""
def measureResistance(DMM):
    #DMM.write("SENS:ZERO:AUTO?")
    print("Initated measurement command")
    DMM.write("MEAS:RES? 1 , .01")
    #sleep(0.25)
    res = DMM.read()
    print("Measured resistance:" + str(res) + " ohms")
    #clear buffer
    DMM.write("*rst; status:preset; *cls")
    return res


if __name__ == '__main__':
                #Setup
                #take user input serial number
                #command == start
                #run automated tesst
                #validate data
                # DeterminePassFail
                #output to csv(create new csv upon recieving a new cable, otherwise update)
                DMM = setup()
                file = get_JSON_file()
                J7_LIST = [x for x in file if x['Tag'] == "J7"]
                J6_LIST = [x for x in file if x['Tag'] == "J6"]
                for J7 in J7_LIST:
                         J7_GPIO_LOW = J7['GPIO_LOW']
                         J7_GPIO_HIGH = J7['GPIO_HIGH']
                         J7_I2C = J7['I2C']
                         for J6 in J6_LIST:
                            J6_I2C = J6['I2C']
                            J6_GPIO_LOW = J6['GPIO_LOW']
                            J6_GPIO_HIGH = J6['GPIO_HIGH']
                            MERGED_GPIO_LOW = list(dict.fromkeys(J7_GPIO_LOW + J6_GPIO_LOW ))
                            MERGED_GPIO_HIGH = list(dict.fromkeys(J7_GPIO_HIGH + J6_GPIO_HIGH))
                            #print("Merged LOW" + str(MERGED_GPIO_LOW))
                           # print("Merged HIGH" + str(MERGED_GPIO_HIGH))
                            GPIO_SETUP(MERGED_GPIO_LOW,MERGED_GPIO_HIGH)
                            I2C_GPIO(J6_I2C,J7_I2C)
                            print(J7['Name'] + "----" + J6['Name'])
                            res = runAutomatedTest(DMM)
                            #break
                            sleep(.25)
                         #break
            
                            #print(str(MERGED_GPIO_HIGH) + "HIGH")
                            #print(str(MERGED_GPIO_LOW) + "LOW")

                #DMM = setup()
                # list_low = ()
                # list_high = (22,24,26)
                #
                # GPIO_SETUP(list_low,list_high)

                # D1_GPA_VAL_J6 = 0
                # D1_GPB_VAL_J6 = 0
                #
            
                # D2_GPB_VAL_J6 = 0
                #
                # D1_GPA_VAL_J7 = 0
                # D1_GPB_VAL_J7 = 0
                #
                # D2_GPA_VAL_J7 = 0x02
                # D2_GPB_VAL_J7 = 0
                #
                # I2C_GPIO(D1_GPA_VAL_J6, D1_GPB_VAL_J6, D2_GPA_VAL_J6, D2_GPB_VAL_J6,D1_GPA_VAL_J7, D1_GPB_VAL_J7, D2_GPA_VAL_J7, D2_GPB_VAL_J7)

                # res = runAutomatedTest(DMM)
                # sleep(1)
                # runAutomatedTest(DMM)

                #createNewCSV("010100",res)






#DMM.write("SENSe:RESistance:RANGe:AUTO?")

