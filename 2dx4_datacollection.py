#2DX4 Project Data collection program

import serial
import math

ser = serial.Serial('COM8',115200) # Change COM Port # to proper
ser.open
print("Opening: " + ser.name)

f = open("2dx4data.xyz", "a") # choosing our file for output 
i = 0
x = 0 #initial x displacment, we take our measurements in y-z plane
increment = 200 # x-displacement increment (mm)
readData = False #at first we are not reading in any data so flag is false

while 1:  
    s = ser.readline()
    curChars = s.decode("utf-8") # Decodes byte input from UART into string 
    curChars = curChars[0:-2] #formatting the byte
    if (curChars.isdigit() == True):
        readData = True #once we decode an integer we can flip this flag and start reading integers
        angle = (i/512)*2*math.pi # Obtain angle based on motor rotation
        d = int(curChars)
        y = d*math.cos(angle) # Calculate y
        z = d*math.sin(angle) # Calculate z
        f.write('{} {} {}\n'.format(x,y,z)) # Write data to .xyz file in this form
        i += 1
    if (curChars.isdigit() == False and readData == True):#if we stop reading integers and read in strings again we must close the file
        f.close()
        f = open("2dx4data.xyz", "a")
    if i == 512:#if i reaches 8 we know we completed one full revolution of measurements
        i = 0
        x = x + increment #since were done with this 360 degrees we need to increment x to correspond to the height difference for manual rotation
    print(curChars)