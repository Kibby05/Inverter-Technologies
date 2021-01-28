import numpy as np
from scipy import signal
from scipy.integrate import *
import matplotlib as mpl
import matplotlib.pyplot as plt
            
def Generate_SPWM_Sig(Ref_Sig, Tri_Sig, t):
    SPWM = np.zeros(len(t))
    for sample in range(len(t)):
        if Ref_Sig[sample] >= Tri_Sig[sample] and Ref_Sig[sample] > 0:
            SPWM[sample] = 1
        elif Ref_Sig[sample] <= Tri_Sig[sample] and Ref_Sig[sample] < 0:
            SPWM[sample] = -1
        else:
            SPWM[sample] = 0
        
    return SPWM

if __name__ == '__main__':
    # Generate Time Stamp for Simulation
    ts = np.linspace(0.0, 1/60, 10000)
    # Generate Traingle Waveform Used for SPWM Generation
    Triangle = signal.sawtooth(2*(np.pi)*6000*ts, 0.5)
    # Generate Grid Reference Signal
    Vgrid = np.sin(2*(np.pi)*60*ts)
    # Generate SPWM Signal
    SPWM = Generate_SPWM_Sig(Vgrid, Triangle, ts)

    # Plot the Output Data
    plt.plot(ts, Triangle, color = 'dodgerblue', label = r'Triangle wave')
    plt.plot(ts, Vgrid, color = 'limegreen', label = r'Vgrid')
    plt.plot(ts, SPWM, color = 'm', label = r'Vspwm')
    plt.xlabel("Time(s)", fontsize=18, style='italic')
    plt.ylabel('SPWM Generation', fontsize=18, style='italic')
    plt.legend(fontsize=18)
    plt.show()

