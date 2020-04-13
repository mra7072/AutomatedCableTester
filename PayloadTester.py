import pyvisa
import time
from time import sleep, strftime, localtime
from datetime import timedelta
import csv
import os
import RPi.GPIO as GPIO
import smbus
from pyvisa.constants import StopBits, Parity
import json
import shutil
from distutils.dir_util import copy_tree

DMM = None
TEST_RESULTS_PATH = "TEST_RESULTS/"
CABLET1 = "J68852"
CABLET2 = "J69068"
CABLET3 = "J69278"
CABLET4 = "J69749"
calibrationState = True
CableState = True
isLeft = True


def runAutomatedTest(DMM):
    return measureResistance(DMM)


def run4AutomatedTest(DMM):
    return measure4Resistance(DMM)


"""
Export results to connected drive 
"""


def exportResults():
    # When USB device is connected it shows up in the following path
    path = "/media/pi"
    if (os.path.exists(path)):
        files = os.listdir(path)
        if (len(files) == 0):
            return False
        else:
            drive = files[0]
            drivepath = path + "/" + drive + "/TEST_RESULTS"
            if os.path.exists(drivepath):
                shutil.rmtree(drivepath)

            os.mkdir(drivepath)
            copy_tree(TEST_RESULTS_PATH, drivepath)
            print("Export successful")
            return True


"""
Performs GPIO intialization on the PI

list_low - specifices pi that are initialized to low
list_high -  specifies pins that are initialized to high
"""


def GPIO_SETUP(list_low, list_high):
    GPIO.setmode(GPIO.BOARD)  # selects by GPIO (e.g GPIO4)

    GPIO.setup(list_low, GPIO.OUT)
    GPIO.setup(list_high, GPIO.OUT)

    GPIO.output(list_low, GPIO.LOW)
    GPIO.output(list_high, GPIO.HIGH)


"""
Performs I2C setup for GPIO Expanders
"""


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


"""
Opens the JSON file with the given filename 
"""


def get_JSON_file(filename):
    with open(filename + ".json") as f:
        data = json.load(f)
        return data


"""
Creates a resource manager and performs proper connection to multimeter device.
Sets parameters
"""


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

    # set read/write terminators to dictate end of command"
    DMM.read_termination = '\n'
    DMM.write_termination = '\n'
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


"""
Issues a measurement command in 4-wire mode, performs measurement, and returns measurement value
"""


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


"""
Initialize directories for all cable types for results storage 
"""


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
Creates a new CSV file for the cable tested
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
    filewriter.writerow(
        ['Configuration', 'Measured-Resistance', 'Expected Resistance', 'Pass/Fail', 'Expected Real Resistance'])

    return filewriter


"""
Default validation for valid connections that is used if calibration file doesnt exist for the cable type
"""


def defaultValidateConnection(res):
    if res >= 5:
        # TODO for repeated test
        return False
    else:
        return True


"""
Default validation for open connections that is used if calibration file doesnt exist for the cable type
"""


def defaultValidateOpen(res):
    if res >= 10000:
        return True
    else:
        return False


"""
Determines and extracts real resistance 
"""


def getExpectedRealRes(res, expectedRes):
    # take difference
    diff = abs(0.1 - abs(res - expectedRes))
    return diff


"""
Validates proper connections with expected resistances
"""


def ValidateConnection(res, expectedRes):
    # take difference
    diff = abs(expectedRes - res)
    tol = 0.1
    if diff >= tol:
        # TODO for repeated test
        return False
    else:
        return True


"""
Validates open connections with their expected resistances
"""


def ValidateOpen(res, expectedRes):
    diff = abs(expectedRes - res)
    tol = 1000
    if diff >= tol:
        return False
    else:
        return True


"""
Grabs the respective JSON file for the cabletype
"""


def load_config(CableType):
    return get_JSON_file(CableType)


"""
Creates JSON file after calibration executes to hold calibration results
"""


def create_lut(CableType, dict):
    # Serializing json
    json_object = json.dumps(dict, indent=4)
    # Writing to json
    with open(CableType + "_" + "Calibration.json", "w") as outfile:
        outfile.write(json_object)


"""
Determines the side of the cable to measure according to JSON file
"""


def determine_measure_left_or_right(CableType):
    # whichever one the user starts off with, it will test that one and return
    # the results, after this call is made message should be prompted to swap
    global isLeft
    lut = {}
    file = load_config(CableType)
    J7_LIST = [x for x in file if x['Tag'] == "J7"]
    J6_LIST = [x for x in file if x['Tag'] == "J6"]
    Connections = [x for x in file if x['Tag'] == "Connection_left"][0]
    isLeft = True
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
            res = float(run4AutomatedTest(DMM))  # Assume left
            # take all measurements for left
            lut[name] = res

            if name in Connections['Name'] and res > 1000:
                # if < 1000, for all left good connections,
                # isLeft should stay true
                isLeft = False
                # if a single one is > 1000, we exit and
                # invalidate results
                lut = {}
                # short circuit
                break
        if isLeft == False:
            # short circuit
            break
    if isLeft == False:
        # its not the left, meaning its the right,
        # measure all right, and return results
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
                lut[name] = 1000
                break

    return lut


def performSpecialCalibration(CableType, lut):
    global DMM
    global calibrationState
    if DMM == None:
        DMM = setup()
    global isLeft
    calibrationState = False
    file = load_config(CableType)
    J7_LIST = [x for x in file if x['Tag'] == "J7"]
    J6_LIST = [x for x in file if x['Tag'] == "J6"]
    Connections_left = [x for x in file if x['Tag'] == "Connection_left"][0]
    Connections_right = [x for x in file if x['Tag'] == "Connection_left"][0]

    # could be left or right returned, just
    # test other side now
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
            if isLeft:
                if name not in Connections_left:
                    # so we dont override left results, we override
                    # open results though..do we care?
                    lut[name] = res
                    break
            else:
                if name not in Connections_right:
                    # so we dont override right results, we override
                    # open results though..do we care?
                    lut[name] = res

    create_lut(CableType, lut)
    calibrationState = True


# for validation, check if connection combination exists in
# left_connection + right_connection merged,
# otherwise validateOpen
# now it doesnt matter, which side when they are testing,
# lut holds both left and right values


"""
Performs a full test of the cable and stores results to a JSON file to hold results. These results are used for validation for 
cables for the same type. One calibration file is created for a single cable type.
- Each calibration will override previous results
NOTE - a good cable should be used for accurate results

"""

def performCalibration(CableType):
    global DMM
    global calibrationState
    if DMM == None:
        DMM = setup()
    calibrationState = False
    lut = {}
    # Grab cable configurations
    file = load_config(CableType)
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
            MERGED_GPIO_LOW = list(dict.fromkeys(J7_GPIO_LOW + J6_GPIO_LOW))
            MERGED_GPIO_HIGH = list(dict.fromkeys(J7_GPIO_HIGH + J6_GPIO_HIGH))
            # Grab each combination, initialize respective GPIOS/I2C setup, and take a measurement
            GPIO_SETUP(MERGED_GPIO_LOW, MERGED_GPIO_HIGH)
            I2C_GPIO(J6_I2C, J7_I2C)
            name = J7['Name'] + "-" + J6['Name']
            sleep(.05)
            res = float(run4AutomatedTest(DMM))
            # write to JSON file
            lut[name] = res

    create_lut(CableType, lut)
    calibrationState = True


# load lookup table if exists and test as normal
# otherwise create lookup table
# else compare against default values

"""
Performs the entire test execution and performs CSV file generation
"""


def executeAutomatedTest(SerialNumber, CableType, Date, Time):
    global DMM
    global CableState
    global calibrationState
    CableState = True
    if DMM == None:
        DMM = setup()
    file = load_config(CableType)
    lut = None
    if os.path.exists(CableType + "_" + "Calibration" + ".json"):
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
                # grab each combination, perform GPIO/I2C initiliazation, and take respective measurement
                J6_I2C = J6['I2C']
                J6_GPIO_LOW = J6['GPIO_LOW']
                J6_GPIO_HIGH = J6['GPIO_HIGH']
                MERGED_GPIO_LOW = list(dict.fromkeys(J7_GPIO_LOW + J6_GPIO_LOW))
                MERGED_GPIO_HIGH = list(dict.fromkeys(J7_GPIO_HIGH + J6_GPIO_HIGH))
                GPIO_SETUP(MERGED_GPIO_LOW, MERGED_GPIO_HIGH)
                I2C_GPIO(J6_I2C, J7_I2C)

                # naming scheme for each combination
                name = J7['Name'] + "-" + J6['Name']
                res = float(runAutomatedTest(DMM))
                expectedRes = "N/A"
                expectedRealRes = "N/A"
                if not LUT_EXISTS:
                    if name in Connections['Name']:
                        state = defaultValidateConnection(res)
                    else:
                        state = defaultValidateOpen(res)
                else:
                    expectedRes = lut[name]
                    # Grab corresponding resistance from calibration file, perform validation whether it is an
                    # open/valid connection
                    if name in Connections['Name']:

                        state = ValidateConnection(res, expectedRes)
                        expectedRealRes = getExpectedRealRes(res, expectedRes)
                    else:
                        state = ValidateOpen(res, expectedRes)
                        expectedRealRes = res
                if CableState == True and state == False:
                    CableState = False
                # Write result to CSV file for respective pin-pin combination
                fw.writerow([name, res, expectedRes, "PASS" if state == True else "FAIL", expectedRealRes])  # break

        end_time = time.time()
        Elapsed = end_time - start_time

        # Write metrics regarding cable
        fw.writerow(["Cable Status", "PASS" if CableState == True else "FAIL"])
        fw.writerow(["Total Time Elapsed", Elapsed])
        fw.writerow(["Date Executed", Date])
        fw.writerow(["Time of Execution", Time])
    else:
        print("Calibration does not exist for cable")


