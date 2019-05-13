from math       import sin, pi 
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
f_d = 22050
tmin = 0
tmax = 0.10
dt   = 1/f_d
tlist = mlab.frange(tmin, tmax, dt)
##--------------------------------------------------------
##
##--------------------------------------------------------
def volt_value(t):
	return 1+A*(sin(2*pi*f_s_1*t) + sin(2*pi*f_s_2*t) + sin(2*pi*f_s_3*t) + sin(2*pi*f_s_4*t) + sin(2*pi*f_s_5*t) + sin(2*pi*f_s_6*t))
    # return 1+A*(sin(2*pi*f_s*t))
    # return np.random.random()

voltage = [(volt_value(t)) for t in tlist]
spectrum_1 = rfft(voltage)
##--------------------------------------------------------
##------------------filtering part 1----------------------
##--------------------------------------------------------
class Filter():
    def __init__(self, a_coef, b_coef, n_coef):
        self.a_coef = a_coef
        self.b_coef = b_coef
        self.n_coef = n_coef
    def filter(self, input_data):
        filt_volt = []
        x_z = [0]*(self.n_coef + 1)
        
        for i in range(len(input_data)):
            y   = 0
            for m in range(self.n_coef, 0, -1):
                x_z[m] = x_z[m - 1]

            x_z[0] = input_data[i]*self.a_coef[0]

            for j in range (1, self.n_coef + 1, 1): 
                x_z[0]+= -x_z[j]*self.a_coef[j]

            for k in range (0, self.n_coef + 1, 1):
                y += x_z[k]*self.b_coef[k]

            filt_volt.append(y)

        return filt_volt

##----------------------------------------------------------
##-------------coefficient for first stage------------------
##----------------------------------------------------------
##section #1
a_coef_1_1 = [0.525828543039357776,
             -1.99315287833078858,
              0.997244104076249416]
b_coef_1_1 = [1,
             -1.99631885323521785,
              1] 
##section #2
a_coef_1_2 = [0.98514378788174306,
             -1.9665278007775604,
              0.971680540810641924]
b_coef_1_2 = [1,
             -1.99759749798163111,
              1] 
##section #3
a_coef_1_3 = [1.7899432111289777,
             -0.885200010264396653,
              0]
b_coef_1_3 = [1,
              -1,
              0] 
##----------------------------------------------------------
##-------------coefficient for second stage-----------------
##----------------------------------------------------------
##section #1
a_coef_2_1 = [0.780545597983568928,
             -1.98454172327042144,
              0.998468983060898374]
b_coef_2_1 = [1,
             -1.98640637335991888,
              1] 
##section #2
a_coef_2_2 = [0.780545597983568928,
             -1.98653531191395594,
              0.998576070222813805]
b_coef_2_2 = [1,
             -1.98764535316191138,
              1] 
##section #3
a_coef_2_3 = [1.62751709363638364,
             -1.97321776696518358,
              0.986087001680641895]
b_coef_2_3 = [1,
              -1.98704061332200621,
              1] 
##----------------------------------------------------------
##-------------coefficient for third stage------------------
##----------------------------------------------------------
##section #1
a_coef_3_1 = [0.780545597983568817,
             -1.94490255673515455,
              0.998496105813971191]
b_coef_3_1 = [1,
             -1.94703027431694564,
              1] 
##section #2
a_coef_3_2 = [0.780545597983568817,
             -1.94870398482269636,
              0.998548945297613622]
b_coef_3_2 = [1,
             -1.94949292626011861,
              1] 
##section #3
a_coef_3_3 = [1.6275170936363812,
             -1.93472288180304686,
              0.986087001680639008]
b_coef_3_3 = [1,
              -1.94827606259531683,
              1] 
##--------------------------------------------
##
##--------------------------------------------
section_1_1 = Filter(a_coef_1_1, b_coef_1_1, 2)
section_1_2 = Filter(a_coef_1_2, b_coef_1_2, 2)
section_1_3 = Filter(a_coef_1_3, b_coef_1_3, 1)

section_2_1 = Filter(a_coef_2_1, b_coef_2_1, 2)
section_2_2 = Filter(a_coef_2_2, b_coef_2_2, 2)
section_2_3 = Filter(a_coef_2_3, b_coef_2_3, 2)

section_3_1 = Filter(a_coef_3_1, b_coef_3_1, 2)
section_3_2 = Filter(a_coef_3_2, b_coef_3_2, 2)
section_3_3 = Filter(a_coef_3_3, b_coef_3_3, 2)
##--------------------------------------------
##----filtration for every single section-----
##--------------------------------------------
filt_volt_1 = section_1_1.filter(voltage)
filt_volt_1 = section_1_2.filter(filt_volt_1)
filt_volt_1 = section_1_3.filter(filt_volt_1)

filt_volt_1 = section_2_1.filter(filt_volt_1)
filt_volt_1 = section_2_2.filter(filt_volt_1)
filt_volt_1 = section_2_3.filter(filt_volt_1)

filt_volt_1 = section_3_1.filter(filt_volt_1)
filt_volt_1 = section_3_2.filter(filt_volt_1)
filt_volt_1 = section_3_3.filter(filt_volt_1)

spectrum_2 = rfft(filt_volt_1)


#--------------------------------------------------------
#--------------------plot settings-----------------------
#--------------------------------------------------------

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
       
