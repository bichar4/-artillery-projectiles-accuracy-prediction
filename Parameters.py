import math
def mils2angle(mils):
    return (mils * 180)/(1000*math.pi)

#Gettin firing inputs 
initial_velocity = 684 #m/s
QEradians = mils2angle(456) 


#Getting General Parameters 
dt = 0.01 #seconds



#Getting form factors 
Fl = 0.9076
Ft = 1
Frho = 1
    
height = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,15000,20000,25000,30000,40000,50000,60000,70000,80000]
temperature_C = [15.00,8.50,2.00,-4.49,-10.98,-17.47,-23.96,-30.45,-36.94,-43.42,-49.90,-56.50,-56.50,-51.60,-46.64,-22.80,-2.5,-26.13,-53.57,-74.51]
temperature_K = [(i+273.15) for i in temperature_C]
air_density = [1.225,1.112,1.007,0.9093,0.8194,0.7364,0.6601,0.5900,0.5258,0.4671,0.4135,0.1948,0.08891,0.04008,0.01841,0.003996,0.001027,0.0003097,0.00008283,0.00001846]
mach_number = [0.01,0.60,0.80,0.90,0.95,1.00,1.05,1.10,1.20,1.35,1.50,1.75,2.00]
Cd = [0.144,0.144,0.146,0.167,0.221,0.327,0.383,0.381,0.370,0.353,0.338,0.314,0.294]
CMa = [3.355,3.378,3.571,3.957,3.886,3.682,3.145,3.384,3.424,3.278,3.264,3.201,3.013]
Clp = [-0.023,-0.023,-0.022,-0.021,-0.020,-0.020,-0.020,-0.019,-0.020,-0.020,-0.020,-0.020,-0.021]
CLa = [-1.763,-1.763,-1.783,-1.827,-2.038,-2.153,-2.207,-2.255,-2.325,-2.442,-2.556,-2.692,-2.767]