import numpy as np

class ExponentialLoad:
    """ --------------------
    docstring for Polynomial ZIP Model
    -------------------------"""
    # Polynomial ZIP Model Constructor
    def __init__(self,P0,Q0,V0,np,nq):
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
        return PL, QL 
    