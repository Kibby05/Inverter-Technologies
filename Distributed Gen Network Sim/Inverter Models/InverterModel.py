import numpy as np

# Might need to inherent from IEEE15472018 class to determine it's properties
class SinglePhaseInverter:
    """ --------------------
    docstring for Single-Phase inverter generation source model
    ""
    Active power dynamics are in accordance with...
    ti*dEi/dt = Ke(Ei* - Ebk) - mi(Pi,nom - (PL,bk + Pbk,network))

    Reactive power dynamics are in accordance with...
    wi = wi* + ni(QL,bk + Qbk,network)

    Note:
    The dynamics and set points of the inverter should adhere to the 
    IEEE 1547-2018 requirements

    -------------------------"""
    # SPInverter Constructor
    def __init__(self, ni, mi, Ke, tao, Prated, wn, Ei, init_Phase):
        
        # Droop Gain Set points
        self._ni = ni 				# Rad/s/VAR 
        self._mi = mi 				# V/Watt
        self.Ke = Ke

        # Nominal Operation Set points
        self.wn = wn 				# rad/s
        self.Ei = Ei 				# V p.u.

        # Inverter Control Loop Delay Constant
        self.tao = tao

        # Inverter rated power
        self.Pi = Prated		   	# Rated active power injection
        self.Pnom = 0.8 * Prated      # Nominal active power injection set point
        self.Qimax = Prated * -0.44	 # Max Reactive power injection
        self.Qimin = Prated * 0.44  # Max Reactive power absorption
        
        # Initial Phase
        self.InitPhase = init_Phase
        # self.InitPhase = 2*np.pi()*np.random.random()

    # Droop Curve Functions.... (These should potentially be user defined not fixed?)
    def Inv_VW_DroopCurve(self):
        return lambda P : -1*self._mi*(self.Pnom - P) + self.Ei

    def Inv_fVAR_DroopCurve(self):
        return lambda Q : self._ni*Q + self.wn

    # Single-Phase Invester Dynamics
    ''' Note for usage within a network scenario Pout passed into must account
    for BOTH local and network loading at the buss the inverter is connected to.
    If not this function will need to be overridden.
    The vector for the ODE solver may be quite large on I am not sure whether 
    each differential should be solved individually.

    Each inverter may be assigned a column vector and therefore is required to 
    have a column Id to specify which column vector within the system matrix is 
    assigned to it?? 
    '''
    def Inv_getInvNextState(self, x, t, Pout, Qout):
        dEdt = (self.Ke)*(self.Ei - x[0]) - self._mi*(self.Pnom - Pout) # Pi and Pnom might need to be switched...
        dthetadt = self.wn + self._ni*Qout
        print(dEdt, dthetadt)
        return self.tao*dEdt, dthetadt
    
    def Inv_getInvNextStateWrapper(self):
        return lambda x, t, Pout, Qout : self.Inv_getInvNextState(x, t, Pout, Qout) 
    
    # Single-Phase Inverter Method Check Against droop requirements are needed