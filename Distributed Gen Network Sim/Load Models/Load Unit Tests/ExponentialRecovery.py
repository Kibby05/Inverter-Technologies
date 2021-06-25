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
        self.Pt = ExponentialLoad(S0[0],S0[1],V0,alphaT[0],alphaT[1])
        self.Ps = ExponentialLoad(S0[0],S0[1],V0,alphaS[0],alphaS[1])
        self.x0 = x0
    
    def ERL_getNextState(self, x, t, V):
        SLexps = self.Ps.Exp_LoadPower(V)
        SLexpt = self.Pt.Exp_LoadPower(V)
        return (1/(self.Tp))*(SLexps[0]-SLexpt[0]-x[0]), (1/(self.Tq))*(SLexps[1]-SLexpt[1]-x[1])

    def ERL_getNextStateWrapper(self):
        return lambda x, t, V : self.ERL_getNextState(x, t, V) 
    
    # Note getNextState and getLoadPower are correlated to each other..
    def ERL_getLoadPower(self, x, V):
        SLexp = self.Pt.Exp_LoadPower(V)
        return x[0] + SLexp[0], x[1] + SLexp[1]
