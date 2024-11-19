import time
import pylab
import numpy as np
import RPi.GPIO as GPIO
from DAH import DS18B20
from matplotlib import pyplot as plt


tmp_b = DS18B20( address="28-00000cf7be3e")
tmp_w = DS18B20( address="28-00000d7c6650")
tmp_ref = DS18B20( address="10-000803471e5e")
tmp_ref2 = DS18B20( address="10-000802de0f29")

GPIO.setmode(GPIO.BCM)
Switch = 17
# not using PWM
# GPIO.setup(Switch, GPIO.OUT)
# using PWM
pwm = GPIO.PWM(Switch, 10)

target = 19.5 # set the target the system will try to achieve
# list to store values for plotting
temp_bL = []
temp_wL = []
temp_refL = []
temp_ref2L = []
time_L = []

# appending t=0 values
temp_bL.append(tmp_b.getCelsius())
temp_wL.append(tmp_w.getCelsius())
temp_refL.append(tmp_ref.getCelsius())
temp_ref2L.append(tmp_ref2.getCelsius())
time_L.append(time.time())

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
        self.error = self.setpoint - temp
        self.intergral_error += self.error
        self.deriv_error = (self.error - self.error_last) / 0.5  #step from sim params or sampling
        self.error_last = self.error

        self.output = self.kp*self.error + self.ki*self.intergral_error + self.kd*self.deriv_error
        print(self.output)            

        if self.output < -1:     # should probably make these conditions less strict
             #state = GPIO.HIGH
             state = 100
        elif self.output >= +1: # this 
             #state = GPIO.LOW
            state = 0 
        else:
            if -1 <= self.output <= 0:
                state  = self.output*-100
            elif 0 < self.output < 1:
                state = (1- self.output)*100 
            else:
                break
            
        assert 0 <= state <= 100, "PWM Duty Cycle has invalid value (not within 0-100)"
        return state

# add PID coeffs 
s1 = PID(100, 0, 0, target)

# beginning feedback loop
while len(time_L) < 20:
    state = s1.compute( tmp_b.getCelsius())
    
    #GPIO.output(Switch, state) # will we need a multi-sensor based PID response calculation
    pwm.ChangeDutyCycle( state )

    print('Duty Cycle : '+str(state)+' TEMPS - black: '+str(tmp_b.getCelsius())+', white: '+str(tmp_w.getCelsius())+', ref: '+str(tmp_ref.getCelsius())+', ref2: '+str(tmp_ref2.getCelsius()))
	
    # append values for plotting
	temp_bL.append(tmp_b.getCelsius())
	temp_wL.append(tmp_w.getCelsius())
	temp_refL.append(tmp_ref.getCelsius())
	temp_ref2L.append(tmp_ref.getCelsius())
	time_L.append(time.time())
	time.sleep(0.1)

GPIO.output( Switch, GPIO.LOW )
# plotting collected data => should make this a live plot
fig, ax1 = plt.subplots()
time1 = np.array(time_L)
time_actual = time1 - time1[0]

data_set = np.array([time_actual, temp_bL, temp_wL, temp_refL, temp_ref2L])
np.savetxt('data_set_10s'+str(time.time())+'.txt', data_set)


ax1.plot(time_actual, temp_bL, label='black', color='r')
ax1.plot(time_actual, temp_wL, label='white', color='blue')
ax1.legend()
ax1.set_xlabel('Time [Second]')
ax1.set_ylabel('Temp [Degree C]')
ax1.set_ylim(15, 23)

ax2 = ax1.twinx()
ax2.axhline(target, linestyle='dashed', color='black', alpha=0.5)
ax2.plot(time_actual, temp_refL, label='ref', color='green')
ax2.plot(time_actual, temp_ref2L, label='ref2', color='green')
ax2.legend()
ax2.set_ylabel('Temp [Degree C]')
ax2.set_ylim(15, 23)
fig.tight_layout()
plt.show()