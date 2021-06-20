import numpy as np

class ZIPpolynomialLoad:
    """ --------------------
    docstring for Polynomial ZIP Model
    -------------------------"""
    # Polynomial ZIP Model Constructor
    def __init__(self,P0,Q0,V0,a1,a2,a3,a4,a5,a6):
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
        PL = self.P0 * (self.__a1*(V/self.V0)**2 + self.__a2*(V/self.V0) + self.__a3)
        QL = self.Q0 * (self.__a4*(V/self.V0)**2 + self.__a5*(V/self.V0) + self.__a6)
        return PL, QL 
    
    def ZIP_UnitTest(self, V):
        return self.ZIP_LoadPower(V)