import time
import pylab
import numpy
import RPi.GPIO as GPIO
from DAH import DS18B20
from matplotlib import pyplot as plt

tmp_b = DS18B20( address="28-000005e9a98b")
tmp_w = DS18B20( address="28-00000d7cf96a")
tmp_ref = DS18B20( address="10-000803471e5e")
tmp_ref2 = DS18B20( address="10-000802de0f29")

GPIO.setmode(GPIO.BCM)
Switch = 17
GPIO.setup(Switch, GPIO.OUT)
#time.sleep(1)
#GPIO.output(Switch, GPIO.HIGH)
#time.sleep(10) 
#GPIO.output(Switch, GPIO.LOW)

# list to store values for plotting
temp_b = []
temp_w = []
temp_ref = []
time_l = []
temp_b.append(tmp_b.getCelsius())
temp_w.append(tmp_w.getCelsius())
temp_ref.append(tmp_ref.getCelsius())
time_l.append(time.time())
while len(time_l) < 16:
	GPIO.output(Switch, GPIO.HIGH) 
	time.sleep(5)
	print('black: '+str(tmp_b.getCelsius())+', white: '+str(tmp_w.getCelsius())+', ref: '+str(tmp_ref.getCelsius()))
	temp_b.append(tmp_b.getCelsius())
	temp_w.append(tmp_w.getCelsius())
	temp_ref.append(tmp_ref.getCelsius())
	time_l.append(time.time())
	
	GPIO.output(Switch, GPIO.LOW)

fig, ax1 = plt.subplots()

ax1.plot(time_l, temp_b, label='black', color='r')
ax1.plot(time_l, temp_w, label='white', color='blue')
ax1.legend()
ax1.set_xlabel('Time [Second]')
ax1.set_ylabel('Temp [Degree C]')

ax2 = ax1.twinx()
ax2.plot(time_l, temp_ref, label='ref', color='green')
ax2.legend()
ax2.set_ylabel('Temp [Degree C]')
fig.tight_layout()
plt.show()
