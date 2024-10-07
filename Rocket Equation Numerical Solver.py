import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import solve_ivp

# Define rocket parameters
v_e = 3000    # Effective exhaust velocity (m/s)
m_initial = 100  # Initial total mass of the rocket (kg)
delta_m = 0.1  # Mass flow rate (kg/s)

# Define time range for integration
t_span = (0, 10)

def rocket_equation(t, v):
     delta_v = v_e * np.log(m_initial / (m_initial - delta_m * t))
     return delta_v

solution = solve_ivp(rocket_equation, t_span, [0], dense_output=True)
t_eval = np.linspace(0, 10, 1000)
v = solution.sol(t_eval)

plt.figure(figsize=(10, 6))
plt.plot(t_eval, v[0], label='Rocket Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Rocket Velocity over Time')
plt.grid(True)
plt.legend()
plt.show()