import HyD
from sensors import Sensor
import time


p = HyD.HyDrone("100.96.1.19", 51234)

# put your mouse arrow on the function you will get hint read it carefully
# print(p.getSensorData(Sensor.CPU_TEMPERATURE))
# print(p.getSensorData(Sensor.CPU_TEMPERATURE)[0])
string = "IMUes: Euler angle: (335.1875, 2.25, 1.3125) ,IMUms: Magnetometer (microteslas): (44.875, -0.375, 18.6875)"
# print(p.moveBackward("1200","1200"))
i=0
while True:
    # s = p.sendMessage("GET,ALIM")
    # if ("None" not in s):

    #     print("The x angle: ", s)
    #     i=0
    # i +=1
    # print(i)
    # time.sleep(1)
    allData = p.getSensorData(Sensor.ALL_DATA)
    print(allData)
    time.sleep(2)

# # in this way you can get the value it is either float, int ,or str
# imu = float(p.getSensorData(Sensor.IMU_YAW)[1])
# print(imu*100)

# # this will send a control command to the robot
# # Motor start have 7 seconds delay to let the motors start properly
# p.startMotors()

# # the control command returns a string of what happening
# print(p.stopMotors())
