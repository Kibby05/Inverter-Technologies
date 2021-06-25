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
    def __init__(self, T, x0, S0, V0, alpha):
        super(ExponentialRecoveryLoad, self).__init__()
        self.Tp = T[0]
        self.Tq = T[1]
        self.Pt = ExponentialLoad(S0[0],S0[1],V0, alpha[1])
        self.Ps = ExponentialLoad(S0[0],S0[1],V0, alpha[0])
        self.xp0 = x0[0]
        self.xq0 = x0[1]
    
    def ERL_getNextState(self, x, t, V):
        print('what the fuck again')
        print(t)
        dxpdt = (1/(self.Tp))*(self.Ps.Exp_LoadPower(V)-self.Pt.Exp_LoadPower(V)-x[0])
        dxqdt = (1/(self.Tq))*(self.Ps.Exp_LoadPower(V)-self.Pt.Exp_LoadPower(V)-x[1])
        # The question is whether or not this should be calling ODE int itself...
        # Answer a wrapper function is needed to return the function to be called by odeint
        return [dxpdt,dxqdt]
    
    # Note getNextState and getLoadPower are correlated to each other..
    def ERL_getLoadPower(self, xp, xq, V):
        PL = xp + self.Pt.Exp_LoadPower(V)
        return

    def ERL_getNextStateWrapper(self):
        print('what the fuck')
        return lambda x ,t, V : self.ERL_getNextState(x, t, V)
