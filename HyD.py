  
import CONN
import time
from sensors import Sensor
import threading


class HyDrone:
    def __init__(self, ipAddress, portNumber):
        self.HOST = ipAddress
        self.PORT = portNumber
        self.s = None
        self.intervalTime = 1   
        self.connect = False
        self.z = None

    def von(self):
        while self.connect == True:
            self.s = CONN.setupConnection(self.HOST, self.PORT, self.s)
    
    def disconnectWithRobot(self):
        self.connect = False
        if self.s != None:
            self.s.close()
    
    def connectToRobot(self):
        self.connect = True
        if self.s == None or self.s.close:
            self.z = threading.Thread(target=self.von)
            self.z.start()
    
    def sendMessage(self, message):
        return CONN.sendMessage(message,self.s)

    def startMotors(self):
        """ Start the Motors, the program will sleep for 7 seconds to start the motors
            Parameters
            ----------
            No Parameters Needed
            Returns
            -------
            String
                motor is on
            """
        s = self.sendMessage("CONTROL,MOTOR_ON")
        return s

    def stopMotors(self):
        """ Stop the Motors
                    Parameters
                    ----------
                    No Parameters Needed
                    Returns
                    -------
                    String
                        motor is off
                    """
        return self.sendMessage("CONTROL,MOTOR_OFF")

    def recordVideo(self):
        """ Start Recording Video, the video will be saved on any USB storage with HyDrone name attached to the Robot
                    Parameters
                    ----------
                    No Parameters Needed
                    Returns
                    -------
                    String
                        video recording started
                    """
        return self.sendMessage("CONTROL,START_RECORDING")

    def stopVideoRecoding(self):
        """ Stop Recording Video, the video will be saved on any USB storage with HyDrone name attached to the Robot
                            Parameters
                            ----------
                            No Parameters Needed
                            Returns
                            -------
                            String
                                video recording stop
                            """
        return self.sendMessage("CONTROL,STOP_RECORDING")
   
    def moveForward(self, leftSpeed, rightSpeed):
        """ Move Backward, will move/turn the both motor forward
                            Parameters
                            ----------
                            leftSpeed : int
                                the speed must be between 1000 to 1500
                            rightSpeed : int
                                the speed must be between 1000 to 1500
                            Returns
                            -------
                            String
                                robot is moving forward speed
                            """
        return self.sendMessage("CONTROL,MOVE_FORWARD," + leftSpeed + "," + rightSpeed + "")

    def moveBackward(self, leftSpeed, rightSpeed):
        """ Move Backward, will move/turn the both motor backward
                            Parameters
                            ----------
                            leftSpeed : int
                                the speed must be between 1000 to 1500
                            rightSpeed : int
                                the speed must be between 1000 to 1500
                            Returns
                            -------
                            String
                                robot is moving back speed
                            """
        return self.sendMessage("CONTROL,MOVE_BACKWARD," + leftSpeed + "," + rightSpeed + "")
    
    def moveRight2(self,speed):
        return self.sendMessage("CONTROL,MOVE_RIGH," + speed + "")

    def moveLeft2(self, speed):
        return self.sendMessage("CONTROL,MOVE_LEF," + speed + "")

    def moveRight(self, speed):
        """ Move to the Right, will move/turn the left motor
                            Parameters
                            ----------
                            speed : int
                                the speed must be between 1000 to 1500
                            Returns
                            -------
                            String
                                robot is moving right speed
                            """
        return self.sendMessage("CONTROL,MOVE_RIGHT," + speed + "")

    def moveLeft(self, speed):
        """ Move to the Left, will move turn the right motor
                            Parameters
                            ----------
                            speed : int
                                the speed must be between 1000 to 1500
                            Returns
                            -------
                            String
                                robot is moving left speed
                            """
        self.sendMessage("CONTROL,MOVE_LEFT," + speed + "")

    def collectWaterSample(self, container):
        """ Start Collecting Water to the Container
                                Parameters
                                ----------
                                container : int
                                    the container number must be between 1 to 4
                                Returns
                                -------
                                String
                                    water sampling started container
                                """
        return self.sendMessage("CONTROL,COLLECT_SAMPLE," + container + "")

    def rollMove(self, distance, direction):
        """ Start Moving UnderWater Roller
                                        Parameters
                                        ----------
                                        distance : int
                                            the distance is the number of the holes of the encoder you want it
                                            to move one circle is equal to 48 holes, 48*2 is 96
                                            set is to 96 for one circle
                                        direction : str
                                            to set the direction of the movement "U" for up "D" for down
                                        Returns
                                        -------
                                        String
                                            roll moving to $distance $direction
                                        """
        return self.sendMessage("CONTROL,ROLLMOVE,"+distance+","+direction+"")

    def getSensorData(self, sensorName):
        """ get Sensor data
                                Parameters
                                ----------
                                sensorName : Sensor
                                    you must import Sensor from sensors, and write the sensor name
                                Returns
                                -------
                                String array
                                    ["Sensor Name","Sensor Value"]
                                """
        if "us1" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[0].split(":")
        elif "us2" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[1].split(":")
        elif "us3" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[2].split(":")
        elif "us4" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[3].split(":")
        elif "pitch" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[4].split(":")
        elif "roll" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[5].split(":")
        elif "yaw" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[6].split(":")
        elif "gtyp" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[7].split(":")
        elif "glat" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[8].split(":")
        elif "glon" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[9].split(":")
        elif "galt" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[10].split(":")
        elif "gtime" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[11].split(":")
        elif "bat1v" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[12].split(":")
        elif "bat2v" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[13].split(":")
        elif "magber" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[14].split(":")
        elif "cputemp" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[15].split(":")
        elif "wifisig" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[16].split(":")
        elif "recstate" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[17].split(":")
        elif "calibratState" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[18].split(":")
        elif "dataRecordState" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")[19].split(":")
        elif "all" in sensorName.value:
            return self.sendMessage("GET,ALL").split(",")
        elif "allimu" in sensorName.value:
            return self.sendMessage("GET,ALIM").split(",")

    def startDataRecord(self):
        self.sendMessage("CONTROL,RECORD_DATA")

    def stopDataRecord(self):
        self.sendMessage("CONTROL,STOP_RECORD_DATA")
