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

target = 20 # set the target the system will try to achieve
# list to store values for plotting
temp_bL = []
temp_wL = []
temp_refL = []
time_L = []

# appending t=0 values
temp_b.append(tmp_b.getCelsius())
temp_w.append(tmp_w.getCelsius())
temp_ref.append(tmp_ref.getCelsius())
time_l.append(time.time())

class PID(object):
    def __init__(self, KP, KI, KD, target):
        self.kp = KP         # add determined values
        self.ki = KI
        self.kd = KD
        self.setpoint = target
        self.error = 0
        self.intergral_error = 0    # starting values 
        self.error_last = 0
        self.deriv_error = 0
        self.output = 0
    def compute(self, temp):
        self.error = target - temp
        self.intergral_error += self.error
        self.deriv_error = (self.error - self.error_last) / Time_step  #step from sim params or sampling
        self.error_last = self.error

        self.output = self.kp*self.error + self.ki*self.intergral_error + self.kd*self.deriv_error

        if self.output > 0:     # should probably make these conditions less strict
             state = GPIO.HIGH
        elif self.output < 0:
             state = GPIO.LOW
        # conditions related to timing the peltier => dont power for too long etc.
        # need to do calibration with PWM stuff to see what this has to be

        return state



# beginning feedback loop
while len(time_l) < 20:
	GPIO.output(Switch, PID.compute( tmp_b.getCelsius(), target )) # will we need a multi-sensor based PID response calculation
	print('black: '+str(tmp_b.getCelsius())+', white: '+str(tmp_w.getCelsius())+', ref: '+str(tmp_ref.getCelsius()))
	
    # append values for plotting
    temp_bL.append(tmp_b.getCelsius())
    temp_wL.append(tmp_w.getCelsius())
	temp_refL.append(tmp_ref.getCelsius())
	time_l.append(time.time())


# plotting collected data => should make this a live plot
fig, ax1 = plt.subplots()
time = np.array([time_l])
time_actual = time - time[0]

ax1.plot(time_actual, temp_b, label='black', color='r')
ax1.plot(time_actual, temp_w, label='white', color='blue')
ax1.legend()
ax1.set_xlabel('Time [Second]')
ax1.set_ylabel('Temp [Degree C]')
ax1.ylim(15, 23)

ax2 = ax1.twinx()
ax2.plot(time_l, temp_ref, label='ref', color='green')
ax2.legend()
ax2.set_ylabel('Temp [Degree C]')
ax2.ylim(15, 23)
fig.tight_layout()
plt.show()
