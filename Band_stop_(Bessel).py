from math       import sin, pi 
from matplotlib import pyplot as plt
from matplotlib import mlab
from numpy.fft  import rfft, rfftfreq
from numpy      import abs as np_abs
import numpy as np
##--------------------------------------------------------
##------------------signal settings-----------------------
##--------------------------------------------------------
f_s = 400
A   = 1
##--------------------------------------------------------
##------------------sample settings-----------------------
##--------------------------------------------------------
f_d = 22050
tmin = 0
tmax = 0.060
dt   = 1/f_d
tlist = mlab.frange(tmin, tmax, dt)
##--------------------------------------------------------
##
##--------------------------------------------------------
def volt_value(t):
	return 1+A*(sin(2*pi*f_s*t) + sin(2*pi*(f_s+50)*t) + sin(2*pi*(f_s-50)*t) + sin(2*pi*(f_s+100)*t) + sin(2*pi*(f_s-100)*t))
    # return 1+A*(sin(2*pi*f_s*t))
    # return np.random.random()

voltage = [(volt_value(t)) for t in tlist]
spectrum_1 = rfft(voltage)
##--------------------------------------------------------
##------------------filtering part 1------------------------
##--------------------------------------------------------
filt_volt_1 = []

n_coef = 6                                    
                                                                                                                                                                        
a_coef_1 = [1,
        -5.9558477872,
        14.8240409549,
        -19.7363831476,
        14.8240409549,
        -5.9558477872,
        1]

b_coef_1 = [1,
        5.8477871422,
        -14.2907628238,
        18.6806146799,
        -13.7758867261,
        5.4340133708,
        -0.8957686610] 

x = [0]*(n_coef+1)
y = [0]*(n_coef+1)

for i in range(len(voltage)):
    for j in range(n_coef, 0, -1):
        x[j] = x[j-1]
        y[j] = y[j-1]

    x[0] = voltage[i]
    y[0] = x[0]*a_coef_1[0]

    for m in range(1, n_coef+1, 1):
        y[0] += a_coef_1[m]*x[m] + b_coef_1[m]*y[m]

    filt_volt_1.append(y[0])

spectrum_2 = rfft(filt_volt_1)


##--------------------------------------------------------
##--------------------plot settings-----------------------
##--------------------------------------------------------

fig, ax = plt.subplots(2,2)

ax[0,0].set(xlabel = 'Time',ylabel = 'Voltage', title = 'Without filtering')
ax[0,1].set(xlabel = 'Time',ylabel = 'Voltage', title = 'With filtering')
ax[1,0].set(xlabel = 'Frequency',ylabel = 'Amplitude', title = 'Without filtering')
ax[1,1].set(xlabel = 'Frequency',ylabel = 'Amplitude', title = 'With filtering')

ax[0,0].plot(tlist,voltage)
ax[0,1].plot(tlist,filt_volt_1)
ax[1,0].plot(rfftfreq(len(tlist), 1./f_d), np_abs(spectrum_1)/len(tlist))
ax[1,1].plot(rfftfreq(len(tlist), 1./f_d), np_abs(spectrum_2)/len(tlist))



ax[0,0].grid()
ax[0,1].grid()
ax[1,0].grid()
ax[1,1].grid()
plt.show()
       
