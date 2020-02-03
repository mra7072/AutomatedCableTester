

import csv
import json
import time

def get_JSON_file():
    with open('J68852.json') as f:
          data = json.load(f)
          return data


def ValidateConnection(res):
    if res >= 5:
        #TODO for repeated test
        return False
    else:
        return True



def ValidateOpen(res):
    if res >= 100:
        return False
    else:
        return True

#Combination consists of making I2C and GPIO calls
def createNewCSV(serial):
    # if(os.path.exists(serial + ".csv")):
    #     #just append to newline
    #     append_write = 'a'
    # else:
    #     append_write = 'w'
    #create new file
   csvfile = open(serial + ".csv", "w")
   filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
   filewriter.writerow(['Configuration','Measured-Resistance', 'Expected Resistance', 'Pass/Fail'])

   return filewriter

CableState = True
file = get_JSON_file()
J7_LIST = [x for x in file if x['Tag'] == "J7"]
J6_LIST = [x for x in file if x['Tag'] == "J6"]
Connections = [x for x in file if x['Tag'] == "Connection"][0]
SerialNumber = ""
CableType = " "
fw = createNewCSV("fucku")
start_time = time.time()
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
            #GPIO_SETUP(MERGED_GPIO_LOW,MERGED_GPIO_HIGH)]
            #I2C_GPIO(J6_I2C,J7_I2C)
            #res = runAutomatedTest(DMM)
            res = 0
            name = J7['Name'] + "-" + J6['Name']
            state = True
            if name in Connections['Name']:
                state = ValidateConnection(res)
            else:
                state = ValidateOpen(res)

            if CableState == True and state == False:
                CableState = False

            fw.writerow([name,res, "N/A", "PASS" if state == True else "FAIL"])

end_time = time.time()
Elapsed =  end_time - start_time
print("Time elapsed",Elapsed)

fw.writerow(["Cable Status","PASS" if CableState == True else "FAIL"])
fw.writerow(["Total Time Elapsed", Elapsed])



            #print(state)













#create new Object containning merged parameters and store in hashmap<> hasmap for valids, hashmap for open


            #print("J7 : " + str(J7_I2C), "J6 " + str(J6_I2C))

#print(J6_LIST)

# print(list_low)
# print(list_high)
# print(I2C[2])


#hex(int(D2_GPA_VAL_J6, 16))


# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}




            #print("J7 : " + str(J7_I2C), "J6 " + str(J6_I2C))

#print(J6_LIST)

# print(list_low)
# print(list_high)
# print(I2C[2])


#hex(int(D2_GPA_VAL_J6, 16))


# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
