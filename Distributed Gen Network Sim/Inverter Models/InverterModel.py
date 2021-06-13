import numpy as np

class SinglePhaseInverter:
    """ --------------------
    docstring 
    for
    Inverter
    -------------------------"""
    # SPInverter Constructor
    def __init__(self, ni, mi, tao, Prated, wn, Ei, init_Phase):
        # Droop Gain Set points
        self._ni = ni 				# Rad/s/VAR 
        self._mi = mi 				# V/Watt
        # Nominal Operation Set points
        self.wn = wn 				# rad/s
        self.Ei = Ei 				# V p.u.
        self.tao = tao 			   	# Inverter delay time constants
        # Inverter rated power
        self.Pi = Prated		   	# Rated active power injection
        self.Pnom = 0.8 * Prated      # Nominal active power injection set point
        self.Qimax = Prated * -0.44	 # Max Reactive power injection
        self.Qimin = Prated * 0.44  # Max Reactive power absorption
        # Initial Phase
        self.InitPhase = init_Phase
        # self.InitPhase = 2*np.pi()*np.random.random()
    def SetDroopParams(self, ni, mi):
        self._ni = ni
        self._mi = mi
        pass

    def GetDroopParams(self):
        return self._ni, self._mi      

        
    def DroopCurve(self):
        
        pass