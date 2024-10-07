import ephem
import matplotlib.pyplot as plt
from datetime import datetime
from skyfield.api import utc, load, Topos

station_data = load.tle('https://celestrak.com/NORAD/elements/stations.txt')
iss = station_data['ISS (ZARYA)']
print(iss) 

## Change to your specified time range. Current: 2 hours
time_scale = load.timescale()
minutes = range(60 * 2)
time_range = time_scale.utc(2024, 3, 21, 2, minutes)

altitudes = []
azimuths = []

for t in time_range:
     # Calculate satellite position at each time step
     port_hedland = Topos(latitude='20.3123 S', longitude='118.64498 E')
     orbit = (iss - port_hedland).at(t)
     altitude, azimuth, distance = orbit.altaz()
     
     # Append the altitude and azimuth values to the lists
     altitudes.append(altitude.degrees)
     azimuths.append(azimuth.degrees)

print(altitude, azimuth)

plt.figure(figsize=(10, 5))
plt.plot(azimuths, altitudes, marker='o', linestyle='-')
plt.title("Satellite Path - ISS")
plt.xlabel("Azimuth (degrees)")
plt.ylabel("Altitude (degrees)")
plt.grid(True)
plt.show()


from skyfield import api
from pytz import timezone
import numpy as np

## Change to your time zone
time_zone = timezone('US/Pacific')

station_data = api.load.tle('https://celestrak.com/NORAD/elements/stations.txt')
iss = station_data['ISS (ZARYA)']
print(iss)

# Current time range (in minutes) = 2 days. Change to your values
minutes = range(60 * 24 * 2)
time_scale = api.load.timescale()

## Change to your specified time range
time_range = time_scale.utc(2024, 3, 21, 2, minutes)

# Change to your specified geocoordinates. Current geocoordinates = Port Hedland in Australia 
port_hedland = api.Topos(latitude='20.3123 S', longitude='118.64498 E')
orbit = (iss - port_hedland).at(time_range)
altitude, azimuth, distance = orbit.altaz()
print(f"Altitudes: {altitude}")
print(f"Azimuth: {azimuth}")
print(f"Distance: {distance}")

visible_pass = altitude.degrees > 0
indicies, = visible_pass.nonzero()
boundaries, = np.diff(visible_pass).nonzero()

print(boundaries)

boundaries = boundaries
passes = boundaries.reshape(len(boundaries) // 2, 2)
print(passes)

# Set this value to any index from 0 to len(boundaries)! This represents the pass we want to observe from our list of collected passes
pass_to_observe = 0
specific_pass = passes[pass_to_observe]
rise, set = specific_pass
print(f'ISS Rises at {time_range[0].astimezone(time_zone)}')
print(f'ISS Sets at {time_range[1].astimezone(time_zone)}')

ax = plt.subplot(111, projection='polar')
plt.title("ISS Pass Polar Chart")
ax.set_rlim([0, 100])
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

θ = np.radians(azimuths) # Convert azimuths to radians 
r = 90 - np.array(altitudes)  # Convert altitudes to the required range

ax.plot(θ[rise:set], r[rise:set], 'bo--')

for k in range(rise, set):
     text = time_range[k].astimezone(time_zone).strftime('%H:%M')
     ax.text(θ[k], r[k], text, ha='right', va='bottom')