# HyDrone API
*find more on test.py*

##### The functions you can use
- startMotors()
- stopMotors()
- recordVideo()
- stopRecoding()
- moveRight(1000 to 1500) 
> select a speed from 1000 to 1500, the robot will start moving at 1100
- moveLeft(1000 to 1500)
- collectWaterSample(1 to 4)
- getSensorData(Sensor.SensorName)

```python
import HyD
from sensors import Sensor

p = HyD.HyDrone(ipAddress=,portNumber=)
p.getSensorData(Sensor.ULTRASONIC1)

# it can be like this as well
s = Sensor
p.getSensorData(s.ULTRASONIC1)
```

#### Sensor Names
Sensor List |
-------------|
ULTRASONIC1|
ULTRASONIC2|
ULTRASONIC3|
ULTRASONIC4|
IMU_PITCH|
IMU_ROLL|
IMU_YAW|
GPS_SIGNAL_TYPE|
GPS_LATITUDE|
GPS_LONGITUDE|
GPS_ALTITUDE|
GPS_TIME|
BATTERY1_VOLTAGE|
BATTERY2_VOLTAGE|
COMPASS_BEARING|
CPU_TEMPERATURE|
WIFI_SIGNAL_STRENGTH|
RECORDING_STATE|
ALL_DATA|
