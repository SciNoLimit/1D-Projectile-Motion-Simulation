import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from scipy.integrate import odeint
#from tkinter import *
import matplotlib

plt.style.use('seaborn')

Mass = float(input('Enter  mass of the particle : '))  # kg
Drag_Coefficient = float(input('Enter Drag Coefficient : ')) # N sec/m
Acceleration_Due_to_Gravity = 9.81  # m/s^2

# Initial Conditions
Lunching_Velocity = float(input('Enter lunching velocity of the particle : '))  # m/s
Init_Height = 0  # m
Initial_Conditions = [Init_Height, Lunching_Velocity]
# print(Initial_Conditions)

dt = float(input('Enter Delta T (0.5 to 0.01 recomended): '))
tMax = (Lunching_Velocity)/4+dt
time = np.arange(0, tMax, dt)  # sec
# print(time)

def diffn_eqn(Parameter, t, Mass, Drag_Coefficient, Acceleration_Due_to_Gravity):
    Height = Parameter[0]
    Velocity = Parameter[1]
    dhdt = Velocity
    d2hdt2 = -Acceleration_Due_to_Gravity-(Drag_Coefficient/Mass)*Velocity
    Solution = [[],[]]
    Solution[0] = dhdt
    Solution[1] = d2hdt2
    return Solution


Height_of_Partical = [Init_Height]   # m
Velocity_of_Partical = [Lunching_Velocity]   # m/s
Time = [time[0]]


for i in range(len(time)):
    if not Height_of_Partical[i]<0:
        tSteps = [time[i], time[i+1]]
        Soln_for_H_and_V = odeint(diffn_eqn, Initial_Conditions, tSteps, (Mass, Drag_Coefficient, Acceleration_Due_to_Gravity))
        Initial_Conditions = Soln_for_H_and_V[1,:]
        Height_of_Partical.append(Initial_Conditions[0])
        Velocity_of_Partical.append(Initial_Conditions[1])
        Time.append(tSteps[1])
        # print(len(Height_of_Partical),"    ",len(Time), "    ",len(Velocity_of_Partical))
    else:
        break
# print(Height_of_Partical)

Ground = np.zeros(len(Height_of_Partical))

fig, (axH, axV) = plt.subplots(nrows= 1, ncols= 2, sharex= False)
plt.subplots_adjust(left = 0.1, bottom = 0.405)
axH.set_title('1D Projectile Motion Simulation')
#plt.tight_layout()
axV.set_xlabel('Time')
axH.set_xlabel('Time')
axH.set_ylabel('Height')
axV.set_ylabel('Velocity')

H = axH.plot(Time[0],Height_of_Partical[0], 'r', label = 'Rate of change of Height')
V = axV.plot(Time[0],Velocity_of_Partical[0], 'b', label = 'Rate of change of Velocity')

axH.legend()
axV.legend()

dataSkip = int(len(Time)//10)+1
# print(dataSkip)

def Refresh_H_and_V(i):
    H = axH.plot(Time[0:i+dataSkip],Height_of_Partical[0:i+dataSkip], 'r')
    V = axV.plot(Time[0:i+dataSkip],Velocity_of_Partical[0:i+dataSkip], 'b')
    
    return H, V

animate_H_and_V = FuncAnimation(fig, Refresh_H_and_V, repeat = False, frames = np.arange(0, (len(Time)+10), dataSkip), interval = 100)

Hmax = "Maximum Height : " + str(np.round(np.max(Height_of_Partical)))
T_of_Flight = "Time of flight : " + str(np.round(Time[-1]))

Hmax_config = plt.axes([0.11, 0.25, 0.25, 0.04])
Hmax_label = matplotlib.widgets.Button(ax= Hmax_config, label = Hmax)

T_of_Flight_config = plt.axes([0.11, 0.205, 0.25, 0.04])
T_of_Flight_label = matplotlib.widgets.Button(ax= T_of_Flight_config, label = T_of_Flight)

Mass_leb = 'Mass : ' + str(Mass) + ' kg'
Drag_leb = 'Drag Coefficient : ' + str(Drag_Coefficient) + ' N s/m'
Lunch_Velocity_leb = 'Lunching Velocity : ' + str(Lunching_Velocity) + ' m/s'
Delta_T_leb =  'Delta Time : ' + str(dt) + ' sec'

Mass_config = plt.axes([0.538, 0.25, 0.15, 0.04])
Mass_Button = matplotlib.widgets.Button(ax= Mass_config, label = Mass_leb)

Drag_Coefficient_config = plt.axes([0.69, 0.25, 0.25, 0.04])
Drag_Coefficient_Button = matplotlib.widgets.Button(ax= Drag_Coefficient_config, label = Drag_leb)

Lunching_Velocity_config = plt.axes([0.538, 0.205, 0.228, 0.04])
Lunching_Velocity_Button = matplotlib.widgets.Button(ax= Lunching_Velocity_config, label = Lunch_Velocity_leb)

Delta_T_config = plt.axes([0.769, 0.205, 0.19, 0.04])
Delta_T_Button = matplotlib.widgets.Button(ax= Delta_T_config, label = Delta_T_leb)

Save_config = plt.axes([0.538, 0.16, 0.15, 0.04])
Save_Button = matplotlib.widgets.Button(ax= Save_config, label = 'Save')

def save(event):
    fig.savefig('1D.png')
    print('Saved')

Save_Button.on_clicked(save)   

# def PopUp(Title):
#     PopUp = Tk()
#     PopUp.title(Title)

#     disp = Entry(PopUp,)
#     disp.pack()

#PopUp('Set')
plt.show()
