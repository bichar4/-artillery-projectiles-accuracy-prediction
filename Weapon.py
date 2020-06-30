import math

class Weapon():
    def __init__(self):
        self.mass = 43.091
        self.Ixx = 0.1416
        self.TwistRate = 20
        self.Diameter = 0.155
        
    def getMass(self):
        return self.mass
    
    def getDiameter(self):
        return self.Diameter
    
    def getSurfaceArea(self):
        return 0.25*math.pi*(self.Diameter**2)
    
    def getIxx(self):
        return self.Ixx
    
    def setMass(self,mass):
        self.mass = mass
    
    def setDiameter(self,diameter):
        self.Diameter = diameter
    
    def setIxx(self,Ixx):
        self.Ixx = Ixx

    def setTwistRate(self,twistRate):
        self.TwistRate = twistRate
        
    def getInitialSpinRate(self,initial_velocity):
        return 2*math.pi*initial_velocity/(self.TwistRate*self.Diameter)#inital spin rate
    