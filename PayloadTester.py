import pyvisa
import time
from time import sleep, strftime, localtime
from datetime import timedelta
import csv
import os
import threading
import RPi.GPIO as GPIO
import smbus
from pyvisa.constants import StopBits, Parity
import json
import random
import shutil
from glob import glob
from subprocess import check_output, CalledProcessError

DMM = None
TEST_RESULTS_PATH = "TEST_RESULTS/"
CABLET1 = "J68852"
CABLET2 = "J69068"
CABLET3 = "J69278"
CABLET4 = "J69749"
calibrationState = True
CableState = True

def Export():
    return


def runAutomatedTest(DMM):
    return measureResistance(DMM)

def run4AutomatedTest(DMM):
    return measure4Resistance(DMM)



# TODO - Add validation checks against lookuptables
def ValidateData():
    return


def DeterminePassFail():
    # Compare resistance to baseline
    return


def GPIO_SETUP(list_low, list_high):
    # GPIO.output(chan_list, GPIO.LOW) # all LOW
    GPIO.setmode(GPIO.BOARD)  # selects by GPIO (e.g GPIO4)

    GPIO.setup(list_low, GPIO.OUT)

    GPIO.setup(list_high, GPIO.OUT)

    # precedence
    GPIO.output(list_low, GPIO.LOW)
    GPIO.output(list_high, GPIO.HIGH)


#
def I2C_GPIO(J6_LIST, J7_LIST):
    bus = smbus.SMBus(1)
    DEVICE1 = 0x20  # Device address (A0-A2)
    DEVICE2 = 0x21

    D1_GPA_VAL_J6 = int(J6_LIST[0], 16)

    D1_GPB_VAL_J6 = int(J6_LIST[1], 16)

    D2_GPA_VAL_J6 = int(J6_LIST[2], 16)

    D2_GPB_VAL_J6 = int(J6_LIST[3], 16)

    D1_GPA_VAL_J7 = int(J7_LIST[0], 16)
    D1_GPB_VAL_J7 = int(J7_LIST[1], 16)

    D2_GPA_VAL_J7 = int(J7_LIST[2], 16)

    D2_GPB_VAL_J7 = int(J7_LIST[3], 16)

    # Pin direction register
    IODIRA = 0x00
    IODIRB = 0x01

    OLATA = 0x14  # GPA
    OLATB = 0x15  # GPB

    # setting to output mode
    bus.write_byte_data(DEVICE1, IODIRA, 0x00)
    bus.write_byte_data(DEVICE1, IODIRB, 0x00)
    bus.write_byte_data(DEVICE2, IODIRA, 0x00)
    bus.write_byte_data(DEVICE2, IODIRB, 0x00)

    D1_GPA_VAL = D1_GPA_VAL_J6 | D1_GPA_VAL_J7
    D1_GPB_VAL = D1_GPB_VAL_J6 | D1_GPB_VAL_J7
    D2_GPA_VAL = D2_GPA_VAL_J6 | D2_GPA_VAL_J7
    D2_GPB_VAL = D2_GPB_VAL_J6 | D2_GPB_VAL_J7

    bus.write_byte_data(DEVICE1, OLATA, D1_GPA_VAL)
    bus.write_byte_data(DEVICE1, OLATB, D1_GPB_VAL)

    bus.write_byte_data(DEVICE2, OLATA, D2_GPA_VAL)
    bus.write_byte_data(DEVICE2, OLATB, D2_GPB_VAL)


#
#
#


"""
Creates a resource manager and performs proper connection to multimeter device.
Sets parameters
"""


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
    DMM.write("MEAS:FRES? 100 , .00001")
    sleep(0.25)
    res = DMM.read()
    print("Measured resistance:" + str(res) + " ohms")
    # clear buffer
    # DMM.write("*rst; status:preset; *cls")
    return res


def measure4Resistance(DMM):
    # DMM.write("SENS:ZERO:AUTO?")
    print("Initated measurement command")
    DMM.write("MEAS:FRES?  100 , .00001")
    sleep(0.25)
    res = DMM.read()
    print("Measured resistance:" + str(res) + " ohms")
    # clear buffer
    # DMM.write("*rst; status:preset; *cls")
    return res


def InitializeDirectories():
    if not os.path.exists(TEST_RESULTS_PATH):
        os.makedirs(TEST_RESULTS_PATH)
    if not os.path.exists(TEST_RESULTS_PATH + CABLET1):
        os.makedirs(TEST_RESULTS_PATH + CABLET1)
    if not os.path.exists(TEST_RESULTS_PATH + CABLET2):
        os.makedirs(TEST_RESULTS_PATH + CABLET2)
    if not os.path.exists(TEST_RESULTS_PATH + CABLET3):
        os.makedirs(TEST_RESULTS_PATH + CABLET3)
    if not os.path.exists(TEST_RESULTS_PATH + CABLET4):
        os.makedirs(TEST_RESULTS_PATH + CABLET4)


"""
Creates a new CSV file for the cable tested or update existing CSV and append new run
"""


def createNewCSV(serial, cabletype):
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
    filewriter.writerow(['Configuration', 'Measured-Resistance', 'Expected Resistance', 'Pass/Fail','Expected Real Resistance'])

    return filewriter


def defaultValidateConnection(res):
    if res >= 5:
        # TODO for repeated test
        return False
    else:
        return True


def defaultValidateOpen(res):
    if res >= 10000:
        return True
    else:
        return False

def getExpectedRealRes(res, expectedRes):
    # take difference
    diff = abs(0.1 - abs(res - expectedRes))
    return diff

def ValidateConnection(res, expectedRes):
    # take difference
    diff = abs(expectedRes - res)
    tol = 0.1
    if diff >= tol:
        # TODO for repeated test
        return False
    else:
        return True


def ValidateOpen(res, expectedRes):
    diff = abs(expectedRes - res)
    tol = 1000
    if diff >= tol:
        return False
    else:
        return True


def load_config(CableType):
    return get_JSON_file(CableType)


def create_lut(CableType, dict):
    # Serializing json
    json_object = json.dumps(dict, indent=4)
    # Writing to sample.json
    with open(CableType + "_" + "Calibration.json", "w") as outfile:
        outfile.write(json_object)


def performCalibration(CableType):
    global DMM
    global calibrationState
    if DMM == None:
        DMM = setup()
    
    calibrationState = False
#     DMM.write("DISP OFF")
    lut = {}
    file = load_config(CableType)
    J7_LIST = [x for x in file if x['Tag'] == "J7"]
    J6_LIST = [x for x in file if x['Tag'] == "J6"]
    Connections = [x for x in file if x['Tag'] == "Connection"][0]
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
            GPIO_SETUP(MERGED_GPIO_LOW, MERGED_GPIO_HIGH)
            I2C_GPIO(J6_I2C, J7_I2C)
            name = J7['Name'] + "-" + J6['Name']
            sleep(.05)
            res = float(run4AutomatedTest(DMM))
#             #res = random.randint(0, 100)
            lut[name] = res
            #(.25)
    create_lut(CableType, lut)
    calibrationState = True
    


# load lookup table if exists and test as normal
# otherwise create lookup table
# else compare against default values

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
    global CableState
    global calibrationState
    CableState = True
    if DMM == None:
        DMM = setup()

    #DMM.write("DISP OFF")

    file = load_config(CableType)
    lut = None
    if os.path.exists(CableType + "_" + "Calibration"+ ".json"):
        lut = load_config(CableType + "_" + "Calibration")
    
        LUT_EXISTS = True
        CableState = True
        J7_LIST = [x for x in file if x['Tag'] == "J7"]
        J6_LIST = [x for x in file if x['Tag'] == "J6"]
        Connections = [x for x in file if x['Tag'] == "Connection"][0]
        InitializeDirectories()
        filename = SerialNumber + "_" + Date.replace("/", "_") + "_" + Time.replace(":", "")
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
                GPIO_SETUP(MERGED_GPIO_LOW, MERGED_GPIO_HIGH)
                I2C_GPIO(J6_I2C, J7_I2C)
                name = J7['Name'] + "-" + J6['Name']
                res = float(runAutomatedTest(DMM))
#                 # res = random.randint(0, 100)
                state = True
                expectedRes = "N/A"
                expectedRealRes = "N/A"
                if not LUT_EXISTS:
                    if name in Connections['Name']:
                        state = defaultValidateConnection(res)
                    else:
                         state = defaultValidateOpen(res)
                else:
                    expectedRes = lut[name]
                    if name in Connections['Name']:
                        state = ValidateConnection(res, expectedRes)
                        expectedRealRes = getExpectedRealRes(res,expectedRes)
                        #print(expectedRealRes + "HELLO")
                    else:
                        state = ValidateOpen(res, expectedRes)
                        expectedRealRes = res
#                         #print(expectedRealRes + "HELLO")
# 
                if CableState == True and state == False:
                    CableState = False
                # use default validation methods
                fw.writerow([name, res, expectedRes, "PASS" if state == True else "FAIL", expectedRealRes])  # break
               # sleep(.25)
# # 
        end_time = time.time()
        Elapsed = end_time - start_time
        fw.writerow(["Cable Status", "PASS" if CableState == True else "FAIL"])
        fw.writerow(["Total Time Elapsed", Elapsed])
        fw.writerow(["Date Executed", Date])
        fw.writerow(["Time of Execution", Time])
        #return CableState
    else:
        print("Calibration does not exist for cable")
#
    #return True


import errno
from distutils.dir_util import copy_tree
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)
def copytree2(source,dest):
    os.mkdir(dest)
    dest_dir = os.path.join(dest,os.path.basename(source))
    shutil.copytree(source,dest_dir)
if __name__ == '__main__':
    #print(test1())
    path = "/media/pi"
    if(os.path.exists(path)):
        files = os.listdir(path)
        if(len(files) == 0):
            print("No device connected")
        else:
            drive = files[0]
            drivepath = path + "/" + drive
            print(drivepath)
            files = os.listdir(TEST_RESULTS_PATH)
            print(files)
            #copytree2(TEST_RESULTS_PATH,drivepath)
#             if os.path.exists(drivepath + "/TEST_RESULTS"):
#                    os.rmdir(drivepath + "/TEST_RESULTS")
               
            os.mkdir(drivepath + "/TEST_RESULTS")
            copy_tree(TEST_RESULTS_PATH, drivepath + "/TEST_RESULTS")
            

#             try:
#                 shutil.copytree(TEST_RESULTS_PATH, drivepath)
#             # Directories are the same
#             except shutil.Error as e:
#                 print('Directory not copied. Error: %s' % e)
#             # Any error saying that the directory doesn't exist
#             except OSError as e:
#                 print('Directory not copied. Error: %s' % e)
# 
        
    # executeAutomatedTest()
    # print("hello")
    #performCalibration(CABLET3)
    #executeAutomatedTest("Ser32", CABLET3, "2/28/2020", "1:29pm")
    # executeAutomatedTest("ya", CABLET1, "1/12/2020", "8:00am")

