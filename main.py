from Parameters import *
from TrajectoryComputer import *
from matplotlib import pyplot as plt 
from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')

M107 = Weapon()
Kupondole = LaunchEnvironment()
Kupondole.setWind(0,1000) #range and cross 
Kupondole.setAltitude(0,0)
trajectory = Trajectory_Computer(M107,Kupondole,initial_velocity,QEradians)

x,y,z = trajectory.compute()
print("Range=",trajectory.getProjectile_Range())
print("TOF=",trajectory.getTOF())
print("Impact Velocity = ",trajectory.getImpactVelocity())
print("ImpactAngle = ",trajectory.getImpactAngle())
ax.plot3D(x,z,y)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')