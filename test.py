import HyD
from sensors import Sensor


p = HyD.HyDrone("awwa234.ddns.net", 51234)

# put your mouse arrow on the function you will get hint read it carefully
print(p.getSensorData(Sensor.CPU_TEMPERATURE))
print(p.getSensorData(Sensor.CPU_TEMPERATURE)[0])
print(p.getSensorData(Sensor.CPU_TEMPERATURE)[1])

# in this way you can get the value it is either float, int ,or str
imu = float(p.getSensorData(Sensor.IMU_YAW)[1])
print(imu*100)

# this will send a control command to the robot
# Motor start have 7 seconds delay to let the motors start properly
p.startMotors()

# the control command returns a string of what happening
print(p.stopMotors())
