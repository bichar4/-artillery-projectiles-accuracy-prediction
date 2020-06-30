import math
from Weapon import * 
from helper_functions import *
from LaunchEnvironment import *
from Parameters import *

class Trajectory_Computer:
    

    def __init__(self,weapon,launch_environment,initialvelocity,QEradians):
        
        self.weapon = weapon
        self.launch_environment = launch_environment
        
        
        #air properties interpolation
        self.alt2temp = TwoPointInterceptMapper(height,temperature_K)
        self.temp_a0 = []
        self.temp_a1 = []
        self.temp = []
        
        #velociy components
        self.v = [initialvelocity]
        self.vx = [initial_velocity * math.cos(math.radians(QEradians))]
        self.vy = [initial_velocity * math.sin(math.radians(QEradians))]
        self.vz = [0]
        #acceleration componetents 
        self.ax = [0]
        self.ay = []
        self.az = [0]
        
        #projectile position components
        self.x = [0]
        self.y = [self.launch_environment.getLaunchAltitude()]
        self.z = [0]
        
        self.t = [0]
        self.dt = 0.01  #time step
        #force components 
        self.Fd = []
        self.Fdx = []
        self.Fdy = []
        self.Fdz = []
        self.Flz = []
        
        self.alt2density = TwoPointInterceptMapper(height,air_density)
        self.rho = []
        self.rho_a0 = []
        self.rho_a1 = []
        
        self.v_PA = []
        self.vx_PA = []
        self.vz_PA = []
        
        self.Cd = []
        self.Cd_a0 = []
        self.Cd_a1 = []
        self.mach2Cd = TwoPointInterceptMapper(mach_number,Cd)
        
        self.CLa = []
        self.CLa_a0 = []
        self.CLa_a1 = []
        self.mach2CLa = TwoPointInterceptMapper(mach_number,CLa)
        
        self.CMa = []
        self.CMa_a0 = []
        self.CMa_a1 = []
        self.mach2CMa = TwoPointInterceptMapper(mach_number,CMa)
        
        self.CLp = []
        self.CLp_a0 = []
        self.CLp_a1 = []
        self.mach2CLp = TwoPointInterceptMapper(mach_number,Clp)
        
        self.theta = [QEradians]
        self.phi = []
        self.beta = []      
        self.p = [self.weapon.getInitialSpinRate(initialvelocity)]
    
        self.rolldamp = []
        self.ap = []
        
        self.vm = [] #speed of sound 
        self.mach = []
    
        self.g = self.launch_environment.getGravity() #acceleration due to gravity
        self.fl = 0.9076 #form factor 
        self.ft = 1
        self.frho = 1
         
        self.air_Cp = self.launch_environment.getAir_Cp()
        self.air_Cv = self.launch_environment.getAir_Cv()
        self.k = self.air_Cp/self.air_Cv
        self.R = self.air_Cp - self.air_Cv
        self.range_vx_AG = self.launch_environment.getRangeWind() #m/s, POSITIVE FOR TAIL
        self.cross_vz_AG = self.launch_environment.getCrossWind() #m/s POSITIVE FROM LEFT 
    
    def getInterpolatedPairValue(self,mapper,x,a0_array,a1_array,main_array,constant = 1):
        a0,a1 = mapper.get_intercepts(x)
        a0_array.append(a0)
        a1_array.append(a1)
        main_array.append(constant*mapper.getY_value(x))
    
    def updateTemperature(self):
        self.getInterpolatedPairValue(self.alt2temp,self.y[-1],self.temp_a0,self.temp_a1,self.temp,self.ft)
        
    def updateAirDensity(self):
        self.getInterpolatedPairValue(self.alt2density,self.y[-1],self.rho_a0,self.rho_a1,self.rho,self.frho)


    def updateSoundSpeed(self):
        self.vm.append(math.sqrt(self.k*self.R*self.temp[-1]))
        
    def updateRelativeVelocity(self):
        self.vx_PA.append(self.vx[-1] - self.range_vx_AG)
        self.vz_PA.append(self.vz[-1] - self.cross_vz_AG)
        self.v_PA.append(math.sqrt((self.vx_PA[-1]**2)+(self.vy[-1]**2)+(self.vz_PA[-1])))
        
    def updateMach(self):
        self.mach.append(self.v_PA[-1]/self.vm[-1])
    

    def updateCoefficient_Cd(self):
        self.getInterpolatedPairValue(self.mach2Cd ,self.mach[-1],self.Cd_a0,self.Cd_a1,self.Cd)
    
    def updateCoefficient_CMa(self):
        self.getInterpolatedPairValue(self.mach2CMa ,self.mach[-1],self.CMa_a0,self.CMa_a1,self.CMa)
    
    def updateCoefficient_CLa(self):
        self.getInterpolatedPairValue(self.mach2CLa ,self.mach[-1],self.CLa_a0,self.CLa_a1,self.CLa)
    
    def updateCoefficient_CLp(self):
        self.getInterpolatedPairValue(self.mach2CLp ,self.mach[-1],self.CLp_a0,self.CLp_a1,self.CLp)
        
    def updateBeta(self):
        self.beta.append((8*self.weapon.getIxx()*self.p[-1]*self.g*math.cos(self.theta[-1]))/(math.pi*self.rho[-1]*(self.weapon.getDiameter()**2)*self.CMa[-1]*(self.v_PA[-1]**3)))
    
    def updatephi(self):
        self.phi.append(abs(math.atan(self.vz[-1]/self.vx[-1])))
    #Force computations 
    def updateFd(self):
        self.Fd.append((0.5*self.rho[-1])*((self.v_PA[-1]**2)*self.weapon.getSurfaceArea()*self.Cd[-1]))
    def updateFdx(self):
        self.Fdx.append(self.Fd[-1]*math.cos(self.theta[-1])*math.cos(self.phi[-1]))
    def updateFdy(self):
        self.Fdy.append(self.Fd[-1]*math.sin(self.theta[-1]))
    def updateFdz(self):
        self.Fdz.append(self.Fd[-1]*math.cos(self.theta[-1])*math.sin(self.phi[-1]))
    def updateFlz(self):
        self.Flz.append(self.fl*0.5*self.rho[-1]*(self.v_PA[-1]**2)*self.weapon.getSurfaceArea()*self.CLa[-1]*math.sin(self.beta[-1])*math.cos(self.phi[-1]+self.beta[-1])) 
    def updateForces(self):
        self.updateFd()
        self.updateFdx()
        self.updateFdy()
        self.updateFdz()
        self.updateFlz()
#==============================================================
    #acceleration computations 
    def updateAx(self):
        self.ax.append((-1 * self.Fdx[-1])/self.weapon.getMass())
    
    def updateAy(self):
        self.ay.append((-1*self.g)-(self.Fdy[-1]/self.weapon.getMass()))
    def updateAz(self):
        self.az.append(-1*(self.Flz[-1] - self.Fdz[-1])/self.weapon.getMass())
    
    def updateAcceleration(self):
        self.updateAx()
        self.updateAy()
        self.updateAz()
#==============================================    
    #velocity computations
    def updateVx(self,dt):
        self.vx.append(self.vx[-1]+self.ax[-1]*dt)
        
    def updateVy(self,dt):
        self.vy.append(self.vy[-1]+self.ay[-1]*dt)
        
        
    
    def updateVz(self,dt):
        self.vz.append(self.vz[-1]+self.az[-1]*dt)
        
    def updateVelocity(self):
        self.updateVx(self.dt)
        self.updateVy(self.dt)
        self.updateVz(self.dt)
#===================================================

    #compute velocity and projectile angle next time
    def update_vel_projec(self):
        self.v.append(math.sqrt((self.vx[-1]**2) + (self.vy[-1] ** 2) + (self.vz[-1]**2)))
        self.x.append(self.x[-1] + self.vx[-1] * self.dt)
        self.y.append(self.y[-1] + self.vy[-1] * self.dt)
        self.z.append(self.z[-1] + self.vz[-1] * self.dt)
        
        
        
    def update_rolldamp(self):
        self.rolldamp.append((0.5*self.rho[-1]*(self.v_PA[-1]**2)*self.weapon.getSurfaceArea()*self.weapon.getDiameter()*(self.p[-1]*self.weapon.getDiameter()/self.v_PA[-1])*self.CLp[-1]))
        self.ap.append(self.rolldamp[-1]/self.weapon.getIxx())
        self.p.append(self.p[-1] + self.ap[-1]*self.dt)
    
    def compute(self):

        while(self.y[-1] >= self.launch_environment.getTargetAltitude()):
            self.t.append(self.t[-1]+self.dt)
            self.updateTemperature()
            self.updateAirDensity()
            self.updateSoundSpeed()
            self.updateRelativeVelocity()
            self.updateMach()
            self.updateCoefficient_Cd()
            self.updateCoefficient_CMa()
            self.updateCoefficient_CLa()
            self.updateCoefficient_CLp()
            self.updateBeta()
            self.updatephi()
            self.updateForces()
            self.updateAcceleration()
            self.updateVelocity()
            self.update_vel_projec()
            self.update_rolldamp()
  
            
        return self.x,self.y,self.z
    
    def getProjectile_Range(self):
        projRange = math.sqrt(self.x[-1]**2 + self.z[-1] **2)
        return projRange
    def getTOF(self):
        return self.t[-1]
    def getImpactAngle(self):
        return abs(self.theta[-1])*3200/math.pi
    def getImpactVelocity(self):
        return self.v[-1]
    def getWindDrift(self):
        projrange = getProjectile_Range()
        return self.vz_AG[-1]*(self.t[-1]-(projrange/self.v[0]))
    def getTotalDrift(self):
        windDrift = getWindDrift()
        return math.abs(self.z[-1])+windDrift
    def classtest(self):        
        self.updateTemperature()
        self.updateAirDensity()
        self.updateSoundSpeed()
        self.updateRelativeVelocity()
        self.updateMach()
        self.updateCoefficient_Cd()
        self.updateCoefficient_CMa()
        self.updateCoefficient_CLa()
        self.updateCoefficient_CLp()
        self.updateBeta()
        self.updatephi()
        self.updateForces()
        self.updateAcceleration()
        self.updateVelocity()
        self.update_vel_projec()
        self.update_rolldamp()
        