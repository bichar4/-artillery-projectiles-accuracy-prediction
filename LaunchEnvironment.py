
class LaunchEnvironment():
    def __init__(self):
        self.launch_alt = 0
        self.target_alt = 0
        self.g = 9.81
        self.rangeWind = 0
        self.crossWind = 0
        self.air_Cp = 1005 #J/Kg.K
        self.air_Cv = 718 #J/Kg.K
        
    def getLaunchAltitude(self):
        return self.launch_alt
    
    def setAltitude(self,launch,target):
        self.launch_alt = launch
        self.target_alt = target
        
        
    
    def getTargetAltitude(self):
        return self.target_alt
    
    def getGravity(self):
        return self.g
    
    def getRangeWind(self):
        return self.rangeWind
    
    def getCrossWind(self):
        return self.crossWind
    
    def setWind(self,rangeWind,crossWind):
        self.rangeWind = rangeWind
        self.crossWind = crossWind
    
    def setAirHeatCapacities(self,Cp,Cv):
        self.air_Cp = Cp
        self.air_Cv = Cv
    
    def getAir_Cp(self):
        return self.air_Cp
    
    def getAir_Cv(self):
        return self.air_Cv
    
        
        