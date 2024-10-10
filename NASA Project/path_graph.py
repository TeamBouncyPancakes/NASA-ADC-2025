import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ms_data = pd.read_csv('middle-school-data.csv')

time = ms_data['MISSION ELAPSED TIME (mins)'].to_numpy()

x_values = ms_data['Rx(km)[J2000-EARTH]'].to_numpy()
y_values = ms_data['Ry(km)[J2000-EARTH]'].to_numpy()
z_values = ms_data['Ry(km)[J2000-EARTH]'].to_numpy()

x_velocity = ms_data['Vx(km/s)[J2000-EARTH]'].to_numpy()
y_velocity = ms_data['Vy(km/s)[J2000-EARTH]'].to_numpy()
z_velocity = ms_data['Vz(km/s)[J2000-EARTH]'].to_numpy()

test = np.array(x_velocity**2 + y_velocity**2 + z_velocity**2)

overall_velocity = np.array(np.sqrt(test))
print(overall_velocity)

mass = ms_data['MASS (kg)'].to_numpy()

wpsa = ms_data['WPSA'].to_numpy()
lb_wpsa = ms_data['Link Budget WPSA'].to_numpy()
ds54 = ms_data['DS54'].to_numpy()
lb_ds54 = ms_data['Link Budget DS54'].to_numpy()
ds24 = ms_data['DS24'].to_numpy()
lb_ds24 = ms_data['Link Budget DS24'].to_numpy()
ds34 = ms_data['DS34'].to_numpy()
lb_ds34 = ms_data['Link Budget DS34'].to_numpy()

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')


ax.plot(x_values,y_values,z_values)
plt.show()


