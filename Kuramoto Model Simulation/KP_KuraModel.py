#---------------------------------------------------------------------------#
# The goal of this script is to simulate a Network of Three coupled Oscillators
# Using the Kuramoto Oscillator
# First we need to know what the governing equations are
# d0i/dt = wi + K/N*SUM(sin(0j-0i)) j=0 -> N
# So lets say we where to have a network of three oscillators
# Oscillator 1: d01/dt = w1 + K/3*(sin(01-01)+sin(02-01)+sin(03-01))
# Oscillator 2: d02/dt = w2 + K/3*(sin(01-02)+sin(02-02)+sin(03-02))
# Oscillator 3: d03/dt = w3 + K/3*(sin(01-03)+sin(02-03)+sin(03-03))
# Now K is the coupling between oscillators so we can make this a variable and see how the coupling plays out in the system
# So now we know our dynamics between the three oscillators which are oscillating at their own frequency + the coupling between
# the three oscillators
#---------------------------------------------------------------------------#

import numpy as np
from scipy.integrate import *
import matplotlib as mpl
import matplotlib.pyplot as plt

#Random normally distributed phase and frequency generator (Frequency normal distributed around 58-62Hz and phase 0-360deg)
Rand_Nat_Freq = 4*np.random.random(4) + 58
Rand_Phase = 360*np.random.random(4)


# Oscillator Natural Frequncies in rad/s
#w1 = 2*np.pi*Rand_Nat_Freq[0]
#w2 = 2*np.pi*Rand_Nat_Freq[1]
#w3 = 2*np.pi*Rand_Nat_Freq[2]

w1 = 377
w2 = 377
w3 = 377

#w4 = 2*np.pi*Rand_Nat_Freq[3]

# Set value test case (debug)
# w1 = 377
# w2 = 383.27
# w3 = 364.42
# intheta1 = 0.8203
# intheta2 = 1.4137
# intheta3 = 0.279

# Initializing initial states
#intheta1 = np.deg2rad(Rand_Phase[0])
#intheta2 = np.deg2rad(Rand_Phase[1])
#intheta3 = np.deg2rad(Rand_Phase[2])
#intheta4 = np.deg2rad(Rand_Phase[3])

intheta1 = np.deg2rad(10)
intheta2 = np.deg2rad(45)
intheta3 = np.deg2rad(70)


print('-------------------------------')
print(Rand_Phase)
print(intheta1,intheta2,intheta3)
print('-------------------------------')

# Initialize the coupling strength and the number of network oscillators N value
K = 5
N = 3

# Gather Oscillor instantaneous frequency and phase values values into a list...
nat_freq = []
inst_phase = []

# Network characteristics
def KuraOsc_derivative(state,ts):
	#global nat_freq

	theta1 = state[0]
	theta2 = state[1]
	theta3 = state[2]

	#print(theta1,theta2,theta3)

	dtheta1dt = w1 + K/N*(np.sin(theta2-theta1) + np.sin(theta3-theta1))
	dtheta2dt = w2 + K/N*(np.sin(theta1-theta2) + np.sin(theta3-theta2))
	dtheta3dt = w3 + K/N*(np.sin(theta2-theta3) + np.sin(theta1-theta3))
	#print(dtheta1dt,dtheta2dt,dtheta3dt)

	res = [dtheta1dt,dtheta2dt,dtheta3dt]
	nat_freq.append([dtheta1dt,dtheta2dt,dtheta3dt])
	inst_phase.append([theta1,theta2,theta3])

	return res

# Initialize time increments
ts = np.linspace(0,10,10000)
print(len(ts))

# Initialize oscillator states
state0 = [intheta1,intheta2,intheta3]

# Analyze the dynamics of the network...... not sure if runge kutta or adams method is being used for odeint.?.?.?.?
state = odeint(KuraOsc_derivative, state0, ts, hmax=0.0001)

# Math the created list of oscillator frequencies or dtheta/dt values with the matrix returned from state = odeint()
# nat_freq.insert(0,[w1,w2,w3]) # Use this if initial oscillators frequencies want to be seen on the plot
np_nat_freq = np.array(nat_freq)
np_inst_phase = np.array(inst_phase)

#print(state)
#print(np_nat_freq)
#print(len(np_nat_freq))
A = len(np_nat_freq)
print(A)
t = np.arange(A)
print(len(t))
#print(np_inst_phase)

# Compute the Mag of the phase
#Mag_theta1 = np.sqrt(np.sin(np_inst_phase[:,0])*np.sin(np_inst_phase[:,0]) + np.cos(np_inst_phase[:,0])*np.cos(np_inst_phase[:,0]))
#Mag_theta2 = np.sqrt(np.sin(np_inst_phase[:,1])*np.sin(np_inst_phase[:,1]) + np.cos(np_inst_phase[:,1])*np.cos(np_inst_phase[:,1]))
#Mag_theta3 = np.sqrt(np.sin(np_inst_phase[:,2])*np.sin(np_inst_phase[:,2]) + np.cos(np_inst_phase[:,2])*np.cos(np_inst_phase[:,2]))
#print(Mag_theta1)

Ntheta0 = np.arctan2(np.sin(np_inst_phase[:,0]),np.cos(np_inst_phase[:,0]))
Ntheta1 = np.arctan2(np.sin(np_inst_phase[:,1]),np.cos(np_inst_phase[:,1]))
Ntheta2 = np.arctan2(np.sin(np_inst_phase[:,2]),np.cos(np_inst_phase[:,2]))
#print(Ntheta0)
#print(np_inst_phase[,0])

#plt.plot(t/10000, Ntheta0[:],)
#plt.plot(t/10000, Ntheta1[:])
#plt.plot(t/10000, Ntheta2[:])
#plt.show()

#plt.plot(t/1000, np.cos(np_inst_phase[:,0]))
#plt.plot(t/1000, np.cos(np_inst_phase[:,1]))
#plt.plot(t/1000, np.cos(np_inst_phase[:,2]))
#plt.show()

#plt.plot(X, Y, 'k', label = r'$\theta_{12}^e $', linewidth = 0.3)

#plt.plot(X, Y, 'k-.', label = r'$\theta_{13}^e $', linewidth = 0.6)

#plt.plot(X, Y, 'k--', label = r'$\theta_{23}^e $', linewidth = 0.6)

#plt.xlabel("Negotiation(Iteration)", fontsize=13, style='italic')

#plt.ylabel('Power(W)', fontsize=13, style='italic')

#plt.legend(fontsize=13)

#plt.tight_layout()

#plt.show()
xticks=[-1.0,-0.5,0,0.5,1]
# plt.plot(t/1000, (np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,1])), 'k', label = r'$\theta_{12}^e $', linewidth = 1.2)
plt.plot(t/1000, (np.cos(state[:,0])))
# plt.plot(t/1000, np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,2]), 'k-.', label = r'$\theta_{13}^e $', linewidth = 2.0)
# plt.plot(t/1000, np.cos(np_inst_phase[:,1])- np.cos(np_inst_phase[:,2]), 'k--', label = r'$\theta_{23}^e $', linewidth = 2.0)
plt.xlabel("Time(s)", fontsize=18, style='italic')
plt.ylabel('Phase Error(s)', fontsize=18, style='italic')
plt.xticks(fontsize=18,style='italic')
plt.yticks(xticks,fontsize=18,style='italic')
plt.legend(fontsize=18)
plt.show()



#plt.plot(t/1000, (np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,1])), color = '0.35', dashes = [15,5])
#plt.plot(t/1000, np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,2]), color = '0.65', linestyle ='dotted')
#plt.plot(t/1000, np.cos(np_inst_phase[:,1])- np.cos(np_inst_phase[:,2]), color = 'k')
#plt.show()

#plt.plot(t/10000,np_nat_freq[:,0])
#plt.plot(t/10000,np_nat_freq[:,1])
#plt.plot(t/10000,np_nat_freq[:,2])
#plt.show()




#Osc0PHErr01 = (np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,1])






# Compute the Euclidian Norm of the three phase vectors (According to Javad)
#PhErr = np.sqrt(theta1*theta1 + theta2*theta2 + theta3*theta3)



#Osc0Err01 = np.sqrt(((np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,1]))*(np.cos(np_inst_phase[:,0])- np.cos(np_inst_phase[:,1]))/500))



#plt.plot(t/10000, Osc0Err01)




#plt.show()
#plt.plot(t/10000, np.sin(np_inst_phase[:,0])+np.cos(np_inst_phase[:,0]))
#plt.plot(t/10000, np.sin(np_inst_phase[:,1])+np.cos(np_inst_phase[:,1]))
#plt.plot(t/10000, np.sin(np_inst_phase[:,2])+np.cos(np_inst_phase[:,2]))
#plt.show()

# Now we need to plot the phase error between the oscillators
# Phase error of oscillator 1

#plt.plot(t/10000, np.sin(np_inst_phase[:,0]))
#plt.plot(t/10000, np.sin(np_inst_phase[:,1]))
#plt.plot(t/10000, np.sin(np_inst_phase[:,2]))
#plt.show()

#plt.plot(t/10000, np.cos(np_inst_phase[:,0]))
#plt.plot(t/10000, np.cos(np_inst_phase[:,1]))
#plt.plot(t/10000, np.cos(np_inst_phase[:,2]))
#plt.show()


#plt.plot(xs[:,0], xs[:,1]) # This is for plotting in phase plance
