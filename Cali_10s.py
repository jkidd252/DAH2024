import time
import pylab
import numpy as np
import RPi.GPIO as GPIO
from DAH import DS18B20
from matplotlib import pyplot as plt

# Set up all the addresses and GPIO ports

tmp_b = DS18B20( address="28-000005e9a98b")
tmp_w = DS18B20( address="28-00000d7cf96a")
tmp_ref = DS18B20( address="10-000803471e5e")
tmp_ref2 = DS18B20( address="10-000802de0f29")

GPIO.setmode(GPIO.BCM)
Switch = 17
GPIO.setup(Switch, GPIO.OUT)


# list to store values for plotting
temp_b = []
temp_w = []
temp_ref = []
temp_ref2 = []
time_l = []

# appending t=0 values
temp_b.append(tmp_b.getCelsius())
temp_w.append(tmp_w.getCelsius())
temp_ref.append(tmp_ref.getCelsius())
temp_ref2.append(tmp_ref.getCelsius())
time_l.append(time.time())

# get room temp for 10s 
while len(time_l) < 10:
    time.sleep(1)
    print('black: '+str(tmp_b.getCelsius())+', white: '+str(tmp_w.getCelsius())+', ref: '+str(tmp_ref.getCelsius()))
    
    # append values for plotting
    temp_b.append(tmp_b.getCelsius())
    temp_w.append(tmp_w.getCelsius())
    temp_ref.append(tmp_ref.getCelsius())
    temp_ref2.append(tmp_ref.getCelsius())
    time_l.append(time.time())
    
Average_roomtemp = (np.mean(temp_ref) + np.mean(temp_ref2))/2 # Average room temp
Average_watertemp = (np.mean(temp_b) + np.mean(temp_w))/2 # Average water temp

Calibration_temp = Average_roomtemp - Average_watertemp
print("Calibration for temperature sensors: " + Calibration_temp + "C")

# Code for the uncertaintiy 

Error_roomtemp = np.sqrt((np.std(temp_ref))**2 + (np.std(temp_ref2))**2 + 0.5**2 + 0.5**2)
Error_watertemp = np.sqrt((np.std(temp_b))**2 + (np.std(temp_w))**2 + 0.2**2 + 0.2**2)

Error_calibrationtemp = np.sqrt(Error_roomtemp**2 + Average_watertemp**2)

print("Error on calibration: " + Error_calibrationtemp + "C")