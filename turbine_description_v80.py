from math import sqrt


voltage = 33000.0
rated_power = 2000000.0
rated_current = rated_power / (sqrt(3) * voltage)  # A = Power / sqrt(3) / Voltage. 3 phase.
cutin_wind_speed = 3.0
cutout_wind_speed = 25.0

hub_height = 90.0

rotor_radius = 40.0  # [m]

solidity_rotor = 0.052  # [-] 'Generic' value, based on Peter Jamieson's book - Figure 2.5 - P.53
cd_rotor_idle_vane = 0.4  # [-] 'Generic' value, very dependent on angle of attack and therefore the assumed rotor misalignment
# cd_rotor_idle_failed_pitch = 1.2 # [-]
cd_nacelle = 1.2  # [-] OWTES V66: 1.3, but using a frontal area of 13 m^2
front_area_nacelle = 14.0  # [m^2] Vestas V80 brochure: height for transport 4 m, width 3.4 m, rounded up 14 m^2 to include height including cooler top 5.4 m
max_thrust = 475000.0  # [N] Maximum thrust determined from thrust coefficient curve multiplied with 1.5 amplification factor (determined by Otto for NREL 5 MW turbine)
yaw_to_hub_height = 2.0  # [m] Vestas V80 brochure: height for transport 4 m - On picture, the axis appears to be in the middle of the nacelle.
mass = 98500.0  # [kg] 79 tonne nacelle + 3x 6.5 tonne blades
mass_eccentricity = -2.0  # [m] - in x-direction, so negative when upwind of tower centre - Just a guess - Vestas V80 brochure: Length of nacelle = 10.4 m
yaw_diameter = 2.26  # [m] From OWTES V66
wind_speed_at_max_thrust = 12.0  # [m/s] Horns rev website: 13 m/s - Vestas V80 brochure: 16 m/s, but max thrust appears at 12 m/s
generator_voltage = 690.0  # [V] There are 480 and 690 voltage versions of the V80. The higher voltage is assumed, considering the need of high voltage in the connections to the public grid.
purchase_price = 1500000.0  # [Euro]
warranty_percentage = 15.0  # [%]
