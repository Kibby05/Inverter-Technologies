# Internal Dependencies
from Exponential import ExponentialLoad
from Frequency_Dependent import FreqDependentLoad
from ZIP_Polynomial import ZIPpolynomialLoad
from EPRI_Loadsyn import EPRILoadsyn

# External Dependencies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    
    

def UnitTest():
    # Define Time Row Vector for Unit Test
    N = 100
    
    # Define Voltage Profile to Determine load Characteristics
    Vchar = np.linspace(0.0, 1.5, N)
    
    # Define Unit Test Voltage Step
    Vbus = np.ones(N)
    Vbus[int(N/2):] *= 0.8

    # Define Frequency Disturbance Step
    f = 60*np.ones(N)
    # f[int(N/4):int(3*N/4)] *= 0.90

    # Desired Loads Under Test...
    ZIP_UnitTest(Vchar)
    Exp_UnitTest(Vchar)
    Freq_UnitTest(Vchar, f)
    EPRI_UnitTest(Vchar, f)
    # NOTE: Results are Pass but Comparison data is needed.

    pass

def displayLoad(x,y):
    # Display Active Power vs. Voltage
    plt.plot(x, y[0], color = 'dodgerblue', label = r'Active Power')
    # Display Reactive Power vs. Voltage
    plt.plot(x, y[1], color = 'limegreen', label = r'Reactive Power')
    plt.grid(color='black', linestyle='-', linewidth=1)
    plt.xlabel("Voltage(V)", fontsize=18, style='italic')
    plt.ylabel('P,Q (W, VAR)', fontsize=18, style='italic')
    plt.xticks(fontsize=28,style='italic')
    plt.yticks(fontsize=28,style='italic')
    plt.legend(fontsize=18)
    plt.show()
    pass

if __name__ == '__main__':
    UnitTest()



