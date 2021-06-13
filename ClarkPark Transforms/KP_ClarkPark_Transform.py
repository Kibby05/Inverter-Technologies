import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq
import matplotlib as mpl
import matplotlib.pyplot as plt
            

def Generate_ThreePhaseSig(Vabc, Amplitude, theta, Frequency, Phase, t):

    for i in range(len(t)):
        Vabc[0,i] = Amplitude*np.sin(theta[i] + (Phase*(np.pi/180)))
        Vabc[1,i] = Amplitude*np.sin(theta[i] - ((120)*(np.pi/180)) + (Phase*(np.pi/180)))
        Vabc[2,i] = Amplitude*np.sin(theta[i] + ((120)*(np.pi/180)) + (Phase*(np.pi/180)))
    return Vabc
    
def Clark_Park_Transformation(Vabc, Vdqo, theta, Frequency, PhaseOffset, t):

    for i in range(len(t)):

        Ks = (2/3)*np.matrix([
            [np.cos(theta[i]), np.cos(theta[i]-((2/3)*np.pi)), np.cos(theta[i]+((2/3)*np.pi))],
            [-1*np.sin(theta[i]), -1*np.sin(theta[i]-((2/3)*np.pi)), -1*np.sin(theta[i]+((2/3)*np.pi))],
            [0.5, 0.5, 0.5]
        ])

        # Vabc is now transformed to Vdqo
        Vdqo[:,i] = np.matmul(Ks, Vabc[:,i])

    return Vdqo

if __name__ == '__main__':
    # ----------------------- Script to Test Clark and Park Transformations --------------------- #

    # DC Link Voltage
    Vdc_Gain = 250

    # Inveter Frequency
    Frequency = 60

    # Number of Samples
    N = 100000

    # Sampling Period
    T = (1/Frequency)

    # Generate Time Stamp for Simulation
    ts = np.linspace(0.0, T, N)
    
    # Generate Null Vectors for Simulation
    Vabc = np.zeros((3,len(ts)))
    Vdqo = np.zeros((3,len(ts)))

    # Initialize Angular velocity Vector
    theta = ts*(2*(np.pi)*Frequency)

    # Generate Traingle Waveform Used for SPWM Generation
    Vabc = Generate_ThreePhaseSig(Vabc, Vdc_Gain, theta, 60, 10, ts)

    # # Test the Numpy Clark Park Transformation matrix
    Vdqo = Clark_Park_Transformation(Vabc, Vdqo, theta, 60, 0, ts)
    
    # Plot the Three-Phase ABC Voltage Waveform
    plt.plot(ts, Vabc[0,:], 'k--',  color = 'black', label = r'$V_{A}(t)$')
    plt.plot(ts, Vabc[1,:], 'k--',color = 'blue', label = r'$V_{B}(t)$')
    plt.plot(ts, Vabc[2,:] , color = 'green', label = r'$V_{C}(t)$')
    plt.xlabel("Time(s)", fontsize=18, style='italic')
    plt.ylabel('$V_{inv}(t)$', fontsize=18, style='italic')
    plt.legend(fontsize=18)
    plt.show()

    # Plot the Three-Phase DQ0 Voltage Waveform
    plt.plot(ts, Vdqo[0,:], 'k--',  color = 'black', label = r'$V_{d}(t)$')
    plt.plot(ts, Vdqo[1,:], 'k--',color = 'blue', label = r'$V_{q}(t)$')
    plt.plot(ts, Vdqo[2,:] , color = 'green', label = r'$V_{o}(t)$')
    plt.xlabel("Time(s)", fontsize=18, style='italic')
    plt.ylabel('$V_{inv}(t)$', fontsize=18, style='italic')
    plt.legend(fontsize=18)
    plt.show()
