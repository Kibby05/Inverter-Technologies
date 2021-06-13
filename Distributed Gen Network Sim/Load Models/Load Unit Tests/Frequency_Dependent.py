from ZIP_Polynomial import ZIPpolynomialLoad
from Exponential import ExponentialLoad

class FreqDependentLoad:
    """ --------------------
    docstring for Frequency Dependent Load
    "
    This class is a *composition* USES AGGREGATION of the ZIP_Polynomial class
    and the Exponential class. We need to select which load model
    you would like to use during runtime.
    "
    -------------------------"""
    # FreqDependentLoad Model Constructor
    def __init__(self,kpf, kqf, f0, ZIPpolynomialLoad=None, ExponentialLoad=None):
        # Aggregate Base Load Models into frequency dependence
        self.ZIPLoad = ZIPpolynomialLoad
        self.ExpLoad = ExponentialLoad

        # Instantiate Base Load Models into frequency dependence
        self.__kpf = kpf
        self.__kqf = kqf
        self.__f0 = f0

    def ZIPfreq_LoadPower(self, V, f):
        PL = (self.ZIPLoad.ZIP_LoadPower(V)[0])*(self.Freq_Dependence(f)[0])
        QL = (self.ZIPLoad.ZIP_LoadPower(V)[1])*(self.Freq_Dependence(f)[1])
        return PL, QL
        
    def Expfreq_LoadPower(self, V, f):
        PL = (self.ExpLoad.Exp_LoadPower(V)[0])*(1+self.__kpf*((f-self.__f0)/self.__f0))
        QL = (self.ExpLoad.Exp_LoadPower(V)[1])*(1+self.__kqf*((f-self.__f0)/self.__f0))
        return PL, QL 
    
    def Freq_Dependence(self, f):
        fp = (1+self.__kpf*((f-self.__f0)/self.__f0))
        fq = (1+self.__kqf*((f-self.__f0)/self.__f0))
        return fp, fq
    

Load = FreqDependentLoad(5,4, ZIPpolynomialLoad(1,1,1,1,1,1,1,1,1))
