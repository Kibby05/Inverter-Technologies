# Internal Dependencies
from numpy.core.fromnumeric import size
from Exponential import ExponentialLoad
from Frequency_Dependent import FreqDependentLoad
from ZIP_Polynomial import ZIPpolynomialLoad
from EPRI_Loadsyn import EPRILoadsyn
from ExponentialRecovery import ExponentialRecoveryLoad

# External Dependencies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from array import *


# These should probably be within the proper files...
# Will adjust later.

def ZIP_UnitTest(V):
    '''

    ........ZIP Load Test......
    Status: PASS 

    '''

    ZIP_AC_1 = ZIPpolynomialLoad(
        0.1,
        0.1,
        1.0,
        1.6,
        -2.69,
        2.09,
        12.53,
        -21.1,
        9.58
    )

    # Run ZIP Load Unit Test
    SLZIPchar = ZIP_AC_1.ZIP_UnitTest(V)
    displayLoad(V, SLZIPchar)

    pass
    
def Exp_UnitTest(V):

    '''

    ........Exponential Load Test......
    Status: PASS 

    '''
    EXP_Load_1 = ExponentialLoad(
        1.0,
        1.0,
        1.0,
        2.0,
        2.0
    )
    SLEXPchar = EXP_Load_1.Exp_UnitTest(V)
    displayLoad(V, SLEXPchar)
    pass

def Freq_UnitTest(V,f):
    '''

    ........Frequency Load Test......
    Status: PASS 

    '''
    ZIP_AC_1 = ZIPpolynomialLoad(
        0.1,
        0.1,
        1.0,
        1.6,
        -2.69,
        2.09,
        12.53,
        -21.1,
        9.58
    )

    EXP_Load_1 = ExponentialLoad(
        1.0,
        0.1,
        1.0,
        2.0,
        2.0
    )

    Freq_Load_1 = FreqDependentLoad(
        1.0,
        -2.8,
        60,
        None,
        EXP_Load_1
    )
    SLFreqEXPchar = Freq_Load_1.Expfreq_LoadPower(V, f)
    displayLoad(V, SLFreqEXPchar)
    pass

def EPRI_UnitTest(V, f):
    Epri_Load_1 = EPRILoadsyn(
        1.0,
        60,
        (1.0,0.1),
        (1.0,1.0),
        (0,0),
        (0,0),
        (0.2, 0.485),
        (1.0,-2.8),
        (0.5,0.672),
        (1.9,1.2),
        (1.0,3.0),
        (0.1,0.5)
    )
    SLEPRIchar = Epri_Load_1.EPRI_LoadPower(V, f)
    displayLoad(V, SLEPRIchar)
    pass
    
def ERL_UnitTest(ts, V):
    
    # Define ERL Load Under Test
    ERL_Load1 = ExponentialRecoveryLoad(
        (127.6,75.3),
        (0.3,1),
        (32.28,5.56),
        (1.0),
        (2.26,5.22),
        (0.38,2.68)
    )

    # Loop through and test ERL state solver
    x0 = ERL_Load1.x0
    dxdt = []
    PL = []
    dxdt.append(list(x0))
    PL.append(list(ERL_Load1.ERL_getLoadPower(x0, V[0])))
    
    # Loop through to calculate next states...
    for i in range(len(ts)-1):
        t = [ts[i], ts[i+1]]
        x = odeint(
            ERL_Load1.ERL_getNextStateWrapper(),
            x0,
            t,
            args = (V[i],)
        ) # Return [x-1, x] in numpy array format

        dxdt.append(x[1].tolist())
        PL.append(list(ERL_Load1.ERL_getLoadPower(x[1], V[i])))
        x0 = x[1]

    # Next State and Load Power Vectors
    dxdt = np.array(dxdt)
    PL = np.array(PL)

    # Display Load Response Results
    displayLoad(ts, dxdt)
    displayLoad(ts, PL)

    pass
       
def displayLoad(x,y):
    # Display Active Power vs. Voltage
    plt.plot(x, y[:,0], color = 'dodgerblue', label = r'Active Power')
    # Display Reactive Power vs. Voltage
    plt.plot(x, y[:,1], color = 'limegreen', label = r'Reactive Power')
    plt.grid(color='black', linestyle='-', linewidth=1)
    plt.xlabel("Voltage(V)", fontsize=18, style='italic')
    plt.ylabel('P,Q (W, VAR)', fontsize=18, style='italic')
    plt.xticks(fontsize=28,style='italic')
    plt.yticks(fontsize=28,style='italic')
    plt.legend(fontsize=18)
    plt.show()
    pass


def UnitTest():
    # Define Number of Sample Pointer required
    N = 10000

    # Simulation Total Time (s)
    T_tot = 10000
    
    # Define Time Row Vector to Use
    t = np.linspace(0.0, T_tot, N)
    
    # Define Voltage Profile to Determine load Characteristics
    Vchar = np.linspace(0.0, T_tot, N)
    
    # Define Unit Test Voltage Step
    Vbus = np.ones(N)
    Vbus[int(N/2):] *= 0.8

    # Define Frequency Disturbance Step
    f = 60*np.ones(N)
    # f[int(N/4):int(3*N/4)] *= 0.90

    # Desired Loads Under Test...
    # ZIP_UnitTest(Vchar)
    # Exp_UnitTest(Vchar)
    # Freq_UnitTest(Vchar, f)
    # EPRI_UnitTest(Vchar, f)
    # ERL_UnitTest(t, Vbus)
    # NOTE: Results are Pass but Comparison data is needed.
    pass



if __name__ == '__main__':
    UnitTest()



