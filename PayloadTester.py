import pyvisa
import time
import atexit
from time import sleep, strftime, localtime
from datetime import timedelta
import csv
import os
import threading
# import RPi.GPIO as GPIO
# import smbus
from pyvisa.constants import StopBits, Parity
import json
import random

"""
Creates a resource manager and performs proper connection to multimeter device.
Sets parameters
"""

DMM = None
TEST_RESULTS_PATH = "TEST_RESULTS"
CABLET1 = "J68852"
CABLET2 = "J69068"
CABLET3 = "J69278"
CABLET4 = "J69749"


def runAutomatedTest(DMM):
    return measureResistance(DMM)


# TODO - Add validation checks against lookuptables
def ValidateData():
    return


def DeterminePassFail():
    # Compare resistance to baseline
    return


# def GPIO_SETUP(list_low,list_high):
#
#    # GPIO.output(chan_list, GPIO.LOW) # all LOW
#     GPIO.setmode(GPIO.BOARD) #selects by GPIO (e.g GPIO4)
#
#     GPIO.setup(list_low, GPIO.OUT)
#
#     GPIO.setup(list_high, GPIO.OUT)
#
#     #precedence
#     GPIO.output(list_low,GPIO.LOW)
#     GPIO.output(list_high,GPIO.HIGH)
#

#
# def I2C_GPIO(J6_LIST, J7_LIST):
#     bus = smbus.SMBus(1)
#     DEVICE1 = 0x20 # Device address (A0-A2)
#     DEVICE2 = 0x21
#
#     D1_GPA_VAL_J6 =   int(J6_LIST[0], 16)
#
#     D1_GPB_VAL_J6 =   int(J6_LIST[1], 16)
#
#
#     D2_GPA_VAL_J6 =   int(J6_LIST[2], 16)
#
#
#     D2_GPB_VAL_J6 =   int(J6_LIST[3], 16)
#
#
#     D1_GPA_VAL_J7 =   int(J7_LIST[0], 16)
#     D1_GPB_VAL_J7 =   int(J7_LIST[1], 16)
#
#     D2_GPA_VAL_J7 =   int(J7_LIST[2], 16)
#
#     D2_GPB_VAL_J7 =   int(J7_LIST[3], 16)
#
#
#     # Pin direction register
#     IODIRA = 0x00
#     IODIRB = 0x01
#
#     OLATA  = 0x14 # GPA
#     OLATB  = 0x15 # GPB
#
#    #setting to output mode
#     bus.write_byte_data(DEVICE1,IODIRA,0x00)
#     bus.write_byte_data(DEVICE1,IODIRB,0x00)
#     bus.write_byte_data(DEVICE2,IODIRA,0x00)
#     bus.write_byte_data(DEVICE2,IODIRB,0x00)
#
#     D1_GPA_VAL = D1_GPA_VAL_J6 | D1_GPA_VAL_J7
#     D1_GPB_VAL = D1_GPB_VAL_J6 | D1_GPB_VAL_J7
#     D2_GPA_VAL = D2_GPA_VAL_J6 | D2_GPA_VAL_J7
#     D2_GPB_VAL = D2_GPB_VAL_J6 | D2_GPB_VAL_J7
#
#     bus.write_byte_data(DEVICE1,OLATA,D1_GPA_VAL)
#     bus.write_byte_data(DEVICE1,OLATB,D1_GPB_VAL)
#
#     bus.write_byte_data(DEVICE2,OLATA,D2_GPA_VAL)
#     bus.write_byte_data(DEVICE2,OLATB,D2_GPB_VAL)
#
#
#


def get_JSON_file(filename):
    with open(filename + ".json") as f:
        data = json.load(f)
        return data


def setup():
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    print(resources)
    print(rm)
    if resources == None:
        print("No connected devices found")
    global DMM
    DMM = rm.open_resource('ASRL/dev/ttyS0::INSTR',
                           baud_rate=9600, data_bits=8,
                           parity=Parity.none, stop_bits=StopBits.one)
    # DMM.write("SYST:REM")
    # sleep(1)
    # clear buffers

    # set read/write terminators to dictate end of command"
    DMM.read_termination = '\n'
    DMM.write_termination = '\n'
    # DMM.write("*rst; status:preset; *cls")
    # Enable remote mode to interface with multimeter
    sleep(1)
    DMM.write("*IDN?")

    sleep(1)
    print("Connection Established with " + DMM.read())
    DMM.write("*rst; status:preset; *cls")
    return DMM


"""
Issues a measurement command, performs measurement, and returns measurement value
"""


def measureResistance(DMM):
    # DMM.write("SENS:ZERO:AUTO?")
    print("Initated measurement command")
    DMM.write("MEAS:RES? 1 , .01")
    # sleep(0.25)
    res = DMM.read()
    print("Measured resistance:" + str(res) + " ohms")
    # clear buffer
    # DMM.write("*rst; status:preset; *cls")
    return res


def InitializeDirectories():
    if not os.path.exists(TEST_RESULTS_PATH):
        os.makedirs(TEST_RESULTS_PATH)
    if not os.path.exists(TEST_RESULTS_PATH + "/" + CABLET1):
        os.makedirs(TEST_RESULTS_PATH + "/" + CABLET1)
    if not os.path.exists(TEST_RESULTS_PATH + "/" + CABLET2):
        os.makedirs(TEST_RESULTS_PATH + "/" + CABLET2)
    if not os.path.exists(TEST_RESULTS_PATH + "/" + CABLET3):
        os.makedirs(TEST_RESULTS_PATH + "/" + CABLET3)
    if not os.path.exists(TEST_RESULTS_PATH + "/" + CABLET4):
        os.makedirs(TEST_RESULTS_PATH + "/" + CABLET4)


"""
Creates a new CSV file for the cable tested or update existing CSV and append new run
"""


def createNewCSV(serial, cabletype):
    #     #just append to newline
    #     append_write = 'a'
    # else:
    #     append_write = 'w'
    # create new file
    path = ""

    if cabletype == CABLET1:
        path = os.path.join(TEST_RESULTS_PATH + "/" + CABLET1, serial + ".csv")
    if cabletype == CABLET2:
        path = os.path.join(TEST_RESULTS_PATH + "/" + CABLET2, serial + ".csv")
    if cabletype == CABLET3:
        path = os.path.join(TEST_RESULTS_PATH + "/" + CABLET3, serial + ".csv")
    if cabletype == CABLET4:
        path = os.path.join(TEST_RESULTS_PATH + "/" + CABLET4, serial + ".csv")

    print(path)
    csvfile = open(path, "w")
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Configuration', 'Measured-Resistance', 'Expected Resistance', 'Pass/Fail'])

    return filewriter


def ValidateConnection(res):
    if res >= 5:
        # TODO for repeated test
        return False
    else:
        return True


def ValidateOpen(res):
    if res >= 10000:
        return True
    else:
        return False


# TODO - load lookuptables into memory
def load_config(CableType):
    return get_JSON_file(CableType)


def executeAutomatedTest(SerialNumber, CableType, Date, Time):
    print("Entered")
    # Setup
    # take user input serial number
    # command == start
    # run automated tesst
    # validate data
    # DeterminePassFail
    # output to csv(create new csv upon recieving a new cable, otherwise update)
    global DMM
    # if DMM == None:
    #     DMM = setup()
    # DMM.write("DISP OFF")
    file = load_config(CableType)
    CableState = True
    J7_LIST = [x for x in file if x['Tag'] == "J7"]
    J6_LIST = [x for x in file if x['Tag'] == "J6"]
    Connections = [x for x in file if x['Tag'] == "Connection"][0]
    InitializeDirectories()
    filename = SerialNumber + "_" + Date.replace("/","_") + "_" + Time.replace(":", "")
    fw = createNewCSV(filename, CableType)
    start_time = time.time()
    for J7 in J7_LIST:
        J7_GPIO_LOW = J7['GPIO_LOW']
        J7_GPIO_HIGH = J7['GPIO_HIGH']
        J7_I2C = J7['I2C']
        for J6 in J6_LIST:
            J6_I2C = J6['I2C']
            J6_GPIO_LOW = J6['GPIO_LOW']
            J6_GPIO_HIGH = J6['GPIO_HIGH']
            MERGED_GPIO_LOW = list(dict.fromkeys(J7_GPIO_LOW + J6_GPIO_LOW))
            MERGED_GPIO_HIGH = list(dict.fromkeys(J7_GPIO_HIGH + J6_GPIO_HIGH))
            #  GPIO_SETUP(MERGED_GPIO_LOW, MERGED_GPIO_HIGH)
            # I2C_GPIO(J6_I2C, J7_I2C)
            name = J7['Name'] + "-" + J6['Name']
            # res = float(runAutomatedTest(DMM))
            res = random.randint(0, 100)
            state = True
            if name in Connections['Name']:
                state = ValidateConnection(res)
            else:
                state = ValidateOpen(res)

            if CableState == True and state == False:
                CableState = False

            fw.writerow([name, res, "N/A", "PASS" if state == True else "FAIL"])  # break
            sleep(.25)

    end_time = time.time()
    Elapsed = end_time - start_time
    print("bye")
    fw.writerow(["Cable Status", "PASS" if CableState == True else "FAIL"])
    fw.writerow(["Total Time Elapsed", Elapsed])
    fw.writerow(["Date Executed", Date])
    fw.writerow(["Time of Execution", Time])
    return CableState


if __name__ == '__main__':
    # executeAutomatedTest()
    print("hello")
