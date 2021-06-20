from Frequency_Dependent import FreqDependentLoad
from Exponential import ExponentialLoad

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
            None,
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
            None,
            ExponentialLoad(
                K2[0],
                K2[1],
                V0,
                nv2[0],
                nv2[1]
            )
        )

    def EPRI_LoadPower(self, V, f):
        SLz = self.Sz.Exp_LoadPower(V)
        SLi = self.Si.Exp_LoadPower(V)
        SLc = self.Sc
        SLf1 = self.S1.Expfreq_LoadPower(V, f)
        SLf2 = self.S2.Expfreq_LoadPower(V, f)
        PL = SLz[0] + SLi[0] + SLc[0] + SLf1[0] + SLf2[0]
        QL = SLz[1] + SLi[1] + SLc[1] + SLf1[1] + SLf2[1]
        return PL, QL