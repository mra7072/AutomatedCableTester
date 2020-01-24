import json

with open('config.json') as f:
  data = json.load(f)

J7_LIST = [x for x in data if x['Tag'] == "J7"]
J6_LIST = [x for x in data if x['Tag'] == "J6"]

#Combination consists of making I2C and GPIO calls

print(mylist)

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
            print(str(MERGED_GPIO_HIGH) + "HIGH")
            print(str(MERGED_GPIO_LOW) + "LOW")



            #print("J7 : " + str(J7_I2C), "J6 " + str(J6_I2C))

#print(J6_LIST)

# print(list_low)
# print(list_high)
# print(I2C[2])


#hex(int(D2_GPA_VAL_J6, 16))


# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
