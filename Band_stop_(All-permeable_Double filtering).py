import numpy as np
import librosa


import soundfile as sf


f_d = 22050 # sample rate
T   = 10.0    # seconds
f_s_1 = 25.0
f_s_2 = 50.0
f_s_3 = 100.0
f_s_4 = 200.0
f_s_5 = 400.0
f_s_6 = 800.0
t   = np.linspace(0.1, T, int(T*f_d), endpoint = False) # time variable

##-------------------------------------------------------------
##----------extract data from a file and add noise-------------
##-------------------------------------------------------------

voltage, f_d = librosa.load('..\\Digital_filters\\wav\\Clean_file.wav', duration = T)
voltage = voltage + 0.100*(np.sin(2*np.pi*f_s_1*t) + 
						 np.sin(2*np.pi*f_s_2*t) + 
						 np.sin(2*np.pi*f_s_3*t) +
						 np.sin(2*np.pi*f_s_4*t) + 
						 np.sin(2*np.pi*f_s_5*t) + 
						 np.sin(2*np.pi*f_s_6*t))

# sf.write('..\\Digital_filters\\wav\\Signal_with_noise.wav', voltage, f_d, subtype = 'PCM_24')

for i in range(len(voltage)):
	with open ('Signal_with_noise.txt','a') as file:
		file.write(str(voltage[i]) + '\n')

# ##-------------------------------------------------------------
# ##-------------------first filtration--------------------------
# ##-------------------------------------------------------------


# filt_volt = [[],[],[],[],[],[],[]]
# filt_volt[0] = voltage
# f_s = [f_s_1, f_s_2, f_s_3, f_s_4, f_s_5, f_s_6]

# for k in range(6):

# 	k_1 = -round(np.cos(2*np.pi*f_s[k]/f_d),8)
# 	k_2 = 0.98
# 	x_z = [0]*2

# 	for i in range(len(filt_volt[k])):
# 		y = 0.5*(filt_volt[k][i] + (filt_volt[k][i] - x_z[1])*k_2 + x_z[1])
# 		filt_volt[k+1].append(y) 
# 		x_z[1] = (((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i]) - x_z[0])*k_1 + x_z[0]
# 		x_z[0] = (((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i]) - x_z[0])*k_1 + ((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i])

# output = np.array(filt_volt[6])

# sf.write('..\\Digital_filters\\wav\\First_filtration.wav', output, f_d, subtype = 'PCM_24')

# ##-------------------------------------------------------------
# ##------------------second filtration--------------------------
# ##-------------------------------------------------------------

# voltage, f_d = librosa.load('..\\Digital_filters\\wav\\First_filtration.wav', duration = T)
# f_s = [f_s_5, f_s_6]
# filt_volt = [[],[],[]]
# filt_volt[0] = voltage
# x_z = [0]*2
# for k in range(2):

# 	k_1 = -round(np.cos(2*np.pi*f_s[k]/f_d),8)
# 	k_2 = 0.80
# 	x_z = [0]*2

# 	for i in range(len(filt_volt[k])):
# 		y = (0.5*(filt_volt[k][i] + (filt_volt[k][i] - x_z[1])*k_2 + x_z[1]))
# 		filt_volt[k+1].append(y) 
# 		x_z[1] = (((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i]) - x_z[0])*k_1 + x_z[0]
# 		x_z[0] = (((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i]) - x_z[0])*k_1 + ((filt_volt[k][i] - x_z[1])*k_2 + filt_volt[k][i])

# output = np.array(filt_volt[2])
# sf.write('..\\Digital_filters\\wav\\Second_filtration.wav', output, f_d, subtype ='PCM_24')
