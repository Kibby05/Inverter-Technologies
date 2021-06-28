# Internal Dependencies
from InverterModel import SinglePhaseInverter

# External Dependencies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from array import *


def Inverter_UnitTest(ts, PL, QL):
    
    # Define Inverter Under Test
    Inverter1 = SinglePhaseInverter(
        ni = 4,
        mi = 0.833,
        Ke = 2,
        tao = 1.5,
        Prated = 0.7,
        wn = 377,
        Ei = 1.0,
        init_Phase = 3
    )

    # Loop through and test ERL state solver
    prev_states = []
    states = []
    # Initial State
    x0 = (1.0, 377)
    # Add initial state to the list
    prev_states.append(list((0,0)))
    states.append(list(x0))
    
    # Loop through to calculate next states...
    for i in range(len(ts)-1):
        t = [ts[i], ts[i+1]]
        x = odeint(
            Inverter1.Inv_getInvNextStateWrapper(),
            x0,
            t,
            args = (PL[i], QL[i])
        ) # Return [x-1, x] in numpy array format

        prev_states.append(x[1].tolist())
        states.append(x[1].tolist())
        print(i)
        # Current state will become previous state
        x0 = x[1]

    # Next State and Load Power Vectors
    states = np.array(states)

    # Display Load Response Results
    displayLoad(ts, states)

    pass


def displayLoad(x,y):
    # Display Active Power vs. Voltage
    plt.plot(x, y[:,0], color = 'dodgerblue', label = r'Active Power')
    # Display Reactive Power vs. Voltage
    # plt.plot(x, np.sin(y[:,1]), color = 'limegreen', label = r'Reactive Power')
    # plt.grid(color='black', linestyle='-', linewidth=1)
    # plt.xlabel("Voltage(V)", fontsize=18, style='italic')
    # plt.ylabel('P,Q (W, VAR)', fontsize=18, style='italic')
    # plt.xticks(fontsize=28,style='italic')
    # plt.yticks(fontsize=28,style='italic')
    # plt.legend(fontsize=18)
    plt.show()
    pass


def UnitTest():
    # Define Number of Sample Pointer required
    N = 2

    # Simulation Total Time (s)
    T_tot = 1
    
    # Define Time Row Vector to Use
    t = np.linspace(0.0, T_tot, N)
    
    
    # Define Unit Test Voltage Step
    PL = np.ones(N)
    PL[int(N/2):] *= 0.8
    QL = np.ones(N)
    QL[int(N/2):] *= 0.2

    # Define Frequency Disturbance Step
    # f = 60*np.ones(N)
    # # f[int(N/4):int(3*N/4)] *= 0.90

    # Unit Test the Inverter
    Inverter_UnitTest(t, PL, QL)
    # TEST RESULT IS PASS...

    pass

if __name__ == '__main__':
    UnitTest()