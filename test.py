import HyD
from sensors import Sensor
import time


p = HyD.HyDrone("100.96.1.19", 51234)

# put your mouse arrow on the function you will get hint read it carefully
# print(p.getSensorData(Sensor.CPU_TEMPERATURE))
# print(p.getSensorData(Sensor.CPU_TEMPERATURE)[0])
string = "IMUes: Euler angle: (335.1875, 2.25, 1.3125) ,IMUms: Magnetometer (microteslas): (44.875, -0.375, 18.6875)"
p.connectToRobot()
time.sleep(2)
# print(p.moveBackward("1200","1200"))
i=0
p.startMotors()
time.sleep(3)
print("start")
t = time.time()
p.moveForward("1100","1100")
time.sleep(1)
p.moveForward("1000","1000")
# p.sendMessage("CONTROL,MOVE_LEF1,1200")
t=t+10
while time.time()<t:
    s = p.sendMessage("GET,ALIM")
    if ("None" not in s):

       print("The x angle: ", s)
    p.moveForward("1100","1100")
    time.sleep(1)
    p.moveForward("1000","1000")
    # p.moveForward("1100","1100")
    # p.sendMessage("CONTROL,MOVE_LEF1,1200")
    # print(p.getSensorData(Sensor.CPU_TEMPERATURE))
    # print(p.getSensorData(Sensor.BATTERY1_VOLTAGE))
    # print(p.getSensorData(Sensor.GPS_LATITUDE))
    # print(p.getSensorData(Sensor.IMU_YAW))
    # print(i)
    time.sleep(0.2)
   # allData = p.getSensorData(Sensor.IMU_YAW)
   # print(allData)
    # time.sleep(2)

p.moveForward("1000","1000")


time.sleep(1)
p.disconnectWithRobot()
# # # in this way you can get the value it is either float, int ,or str
# imu = float(p.getSensorData(Sensor.IMU_YAW)[1])
# print(imu*100)

# # this will send a control command to the robot
# # Motor start have 7 seconds delay to let the motors start properly
# p.startMotors()

# # the control command returns a string of what happening
# print(p.stopMotors())
