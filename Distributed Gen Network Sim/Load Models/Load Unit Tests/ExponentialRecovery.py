from Exponential import ExponentialLoad


class ExponentialRecoveryLoad:
    """ --------------------
    docstring for ERL dynamic load Model
    "
    Tpdxp/dt + xp = Ps(V) - Pt(V)
    Pl = xp + PTt(V)
    TqDxq/dt + xq = Qs(V) - Qt(V)
    Ql = xq + Qt(V)

    In order to keep the class clean, we denoted the attribute 'Sx' to hold the real and reactive
    parameters as a tuple (Px,Qx).
    Alpha = (alpha transient, alpha static)
    "
    -------------------------"""
    def __init__(self, T, x0, S0, V0, alphaT, alphaS):
        super(ExponentialRecoveryLoad, self).__init__()
        self.Tp = T[0]
        self.Tq = T[1]
        self.Pt = ExponentialLoad(S0[0],S0[1],V0, alphaT)
        self.Ps = ExponentialLoad(S0[0],S0[1],V0, alphaS)
        self.xp0 = x0[0]
        self.xq0 = x0[1]
    
    def ERL_getNextState(self, V, xp, xq):
        dxpdt = (1/(self.Tp))*(self.Ps.Exp_LoadPower(V)-self.Pt.Exp_LoadPower(V)-xp)
        dxqdt = (1/(self.Tq))*(self.Ps.Exp_LoadPower(V)-self.Pt.Exp_LoadPower(V)-xq)
        # The question is whether or not this should be calling ODE int itself...
        return [dxpdt,dxqdt]

    def ERL_getNextStateWrapper(self):
        return lambda V,xp,xq : self.ERL_getNextState(V,xp,xq) 
    
    # Note getNextState and getLoadPower are correlated to each other..
    def ERL_getLoadPower(self, xp, xq, V):
        PL = xp + self.Pt.Exp_LoadPower(V)
        return
