import numpy as np

class ZIPpolynomialLoad:
    """ --------------------
    docstring for Polynomial ZIP Model
    -------------------------"""
    # Polynomial ZIP Model Constructor
    def __init__(self,P0,Q0,V0,a1,a2,a3,a4,a5,a6, **kwargs):
        print("ZIPpolynomialLoad Class")
        super().__init__(**kwargs)
        # Polynomial ZIP Model Intial Conditions (Public)
        self.P0 = P0
        self.Q0 = Q0
        self.V0 = V0
        # Polynomial ZIP Model Coefficients (Private)
        self.__a1 = a1
        self.__a2 = a2
        self.__a3 = a3
        self.__a4 = a4
        self.__a5 = a5
        self.__a6 = a6         

    def ZIP_LoadPower(self, V):
        # Note: We need to pay attenetion with the initial coniditions as well as
        # passing in an array or not...
        PL = self.P0 - (self.__a1*(V/self.V0)^2 + self.__a2*(V/self.V0) + self.__a3)
        QL = self.Q0 - (self.__a4*(V/self.V0)^2 + self.__a5*(V/self.V0) + self.__a6)
        return (PL, QL) 
    
class ExponentialLoad:
    """ --------------------
    docstring for Polynomial ZIP Model
    -------------------------"""
    # Polynomial ZIP Model Constructor
    def __init__(self,P0,Q0,V0,np,nq, **kwargs):
        print("ExponentialLoad Class")
        super().__init__(**kwargs)
        # Polynomial ZIP Model Intial Conditions (Public)
        self.P0 = P0
        self.Q0 = Q0
        self.V0 = V0
        # Polynomial ZIP Model Coefficients (Private)
        self.__np = np
        self.__nq = nq
    
    def Exp_LoadPower(self, V):
        # Note: We need to pay attenetion with the initial coniditions as well as
        # passing in an array or not...
        PL = self.P0*((V/self.V0)^self.__np)
        QL = self.Q0*((V/self.V0)^self.__nq)
        return (PL, QL) 
    

class FreqDependentLoad:
    """ --------------------
    docstring for Frequency Dependent Load
    "
    This class is USES AGGREGATION of the ZIP_Polynomial class
    and the Exponential class. We need to select which load model
    you would like to use during runtime.
    "
    -------------------------"""
    # FreqDependentLoad Model Constructor
    def __init__(self, kpf, kqf, f0, ZIPpolynomialLoad=None, ExponentialLoad=None, **kwargs):
        print("FreqDependentLoad Class")
        super().__init__(**kwargs)
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
    

class EPRILoadsyn:
    """ --------------------
    docstring for EPRI Load Syn Model
    "
    This class uses the OOP principles of aggregation AND composition...

    The EPRI LoadSyn model serves as an extension of the static exponential load models
    and the frequency dependent models.

    In order to keep the class clean, we denoted the attribute 'Sx' to hold the real and reactive
    parameters as a tuple (Px,Qx).
    "
    -------------------------"""
    def __init__(self, V0, f0, S0, Sfrac, 
                Ki, Kc, K1, kf1, K2, kf2, nv1, nv2
                ):
        # Super function added in the use case of multiple inheretence...
        print("EPRILoadsyn Class")
        super().__init__()

        # Initial EPRI Load settings by composing of Exponential classes
        self.Sz = ExponentialLoad(
            (1-(Ki[0]+Kc[0]+K1[0]+K2[0])),
            (1-(Ki[1]+Kc[1]+K1[1]+K2[1])),
            V0,
            2, 
            2 
        )
        self.Si = ExponentialLoad(
            Ki[0], Ki[1],
            V0,
            1,
            1
        )
        self.Sc = (Kc[0], Kc[1])
        self.S1 = FreqDependentLoad(
            kf1[0],
            kf1[1],
            f0,
            ExponentialLoad(
                K1[0],
                K1[1],
                V0,
                nv1[0],
                nv1[1]
            )
        )
        self.S2 = FreqDependentLoad(
            kf2[0],
            kf2[1],
            f0,
            ExponentialLoad(
                K2[0],
                K2[1],
                V0,
                nv2[0],
                nv2[1]
            )
        )

    def EPRI_LoadPower(self, V, f):
        SL = self.Sz.Exp_LoadPower(V) + self.Si.Exp_LoadPower(V) + self.Sc 
        + self.S1.Expfreq_LoadPower(V, f) + self.S2.Expfreq_LoadPower(V,f)
        return SL