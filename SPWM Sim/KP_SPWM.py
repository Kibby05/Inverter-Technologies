import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq
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
    # DC Link Voltage
    Vdc_Gain = 250    
    # Number of Samples
    N = 100000
    # Sampling Period
    T = (1/60)
    # Generate Time Stamp for Simulation
    ts = np.linspace(0.0, T, N)
    # Generate Traingle Waveform Used for SPWM Generation
    Triangle = signal.sawtooth(2*(np.pi)*10000*ts, 0.5)
    Triangle2 = signal.sawtooth(2*(np.pi)*100000*ts, 0.5)
    # Generate Grid Reference Signal
    Vgrid = np.sin(2*(np.pi)*60*ts)
    # Generate SPWM Signal
    SPWM = Generate_SPWM_Sig(Vgrid, Triangle, ts)
    SPWM2 = Generate_SPWM_Sig(Vgrid, Triangle2, ts)
    # Discrete Fourier Transform of SPWM
    SPWM_f = rfft(SPWM)
    SPWM_f2 = rfft(SPWM2)
    Xf = rfftfreq(N, T/N)
    # Plot the SPWM Time Domain Output
    plt.plot(ts, Triangle, 'k--',  color = 'black', label = r'$V_{saw}(t)$')
    plt.plot(ts, Vdc_Gain*Vgrid, 'k--',color = 'black', label = r'$V_{fund}(t)$')
    plt.plot(ts, Vdc_Gain*SPWM , color = 'black', label = r'$V_{inv}(t)$')
    plt.xlabel("Time(s)", fontsize=18, style='italic')
    plt.ylabel('$V_{inv}(t)$', fontsize=18, style='italic')
    plt.legend(fontsize=18)
    plt.show()
    # Plot the SPWM Frequency Domain Output
    plt.plot(Xf/1000, 2/N*np.abs(SPWM_f), 'k--',color = 'dodgerblue', label = r'$V_{spwm}(f) (f_{saw}=10kHz)$')
    plt.plot(Xf/1000, 2/N*np.abs(SPWM_f2),color = 'black', label = r'$V_{spwm}(f) (f_{saw}=100kHz)$')
    plt.xlabel("Frequency (f) kHz", fontsize=18, style='italic')
    plt.ylabel('$|V_{SPWM}|$', fontsize=18, style='italic')
    plt.legend(fontsize=18)
    plt.show()

