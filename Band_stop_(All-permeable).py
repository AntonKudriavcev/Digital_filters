from math       import sin, pi, cos
from matplotlib import pyplot as plt
from matplotlib import mlab
from numpy.fft  import rfft, rfftfreq
from numpy      import abs as np_abs
import numpy as np

##--------------------------------------------------------
##------------------signal settings-----------------------
##--------------------------------------------------------
f_s_1 = 25
f_s_2 = 50
f_s_3 = 100
f_s_4 = 200
f_s_5 = 400
f_s_6 = 800
A   = 1
##--------------------------------------------------------
##------------------sample settings-----------------------
##--------------------------------------------------------
f_d   = 22050
tmin  = 0
tmax  = 0.1
dt    = 1/f_d
tlist = mlab.frange(tmin, tmax, dt)

mean = 0
std = 10

##--------------------------------------------------------
##
##--------------------------------------------------------
def volt_value(t):
	signal_1 = sin(2*pi*f_s_1*t)
	signal_2 = sin(2*pi*f_s_2*t)
	signal_3 = sin(2*pi*f_s_3*t)
	signal_4 = sin(2*pi*f_s_4*t)
	signal_5 = sin(2*pi*f_s_5*t)
	signal_6 = sin(2*pi*f_s_6*t)

	# return 1+A*(signal_1 + signal_2 + signal_3 + signal_4 + signal_5 + signal_6)
	return np.random.normal(mean, std)
	# return 1+A*(sin(2*pi*f_s*t) + sin(2*pi*(f_s+50)*t) + sin(2*pi*(f_s-50)*t) + sin(2*pi*(f_s+100)*t) + sin(2*pi*(f_s-100)*t))
    # return 1+A*(sin(2*pi*f_s*t))

voltage = [(volt_value(t)) for t in tlist]



##--------------------------------------------------------
##-------------------filter part--------------------------
##--------------------------------------------------------

filt_volt = [[],[],[],[],[],[],[]]
filt_volt[0] = voltage
spectrum_1 = rfft(voltage)
f_s = [f_s_1, f_s_2, f_s_3, f_s_4, f_s_5, f_s_6]

for k in range(6):

	k_1 = -round(cos(2*pi*f_s[k]/f_d),8)
	k_2 = 0.98
	x_z = [0]*2

	for i in range(len(filt_volt[k])):
		y = 0.5*(filt_volt[k][i] + (filt_volt[k][i] - x_z[1])*k_2 + x_z[1])
		filt_volt[k+1].append(y) 
		x_z[1] = (((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i]) - x_z[0])*k_1 + x_z[0]
		x_z[0] = (((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i]) - x_z[0])*k_1 + ((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i])


output = filt_volt[6]

spectrum_2 = rfft(output)
for i in range(len(spectrum_2)):
	spectrum_2[i] = 1000*(spectrum_2[i]/spectrum_1[i])
##--------------------------------------------------------
##--------------------plot settings-----------------------
##--------------------------------------------------------

fig, ax = plt.subplots(2,2)

ax[0,0].set(xlabel = 'Time', ylabel = 'Voltage', title = 'Without filtering')
ax[0,1].set(xlabel = 'Time', ylabel = 'Voltage', title = 'With filtering')
ax[1,0].set(xlabel = 'Frequency', ylabel = 'Amplitude', title = 'Without filtering')
ax[1,1].set(xlabel = 'Frequency', ylabel = 'Amplitude', title = 'With filtering')

ax[0,0].plot(tlist,voltage)
ax[0,1].plot(tlist,output)
ax[1,0].plot(rfftfreq(len(voltage), 1./f_d), np_abs(spectrum_1)/(len(tlist)/2))
ax[1,1].plot(rfftfreq(len(output),  1./f_d), np_abs(spectrum_2)/(len(tlist)/2))

ax[0,0].grid()
ax[0,1].grid()
ax[1,0].grid()
ax[1,1].grid()
plt.show()
     