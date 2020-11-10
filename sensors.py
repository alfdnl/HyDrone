from enum import Enum


class Sensor(Enum):
    ULTRASONIC1 = "us1"
    ULTRASONIC2 = "us2"
    ULTRASONIC3 = "us3"
    ULTRASONIC4 = "us4"
    IMU_PITCH = "pitch"
    IMU_ROLL = "roll"
    IMU_YAW = "yaw"
    GPS_SIGNAL_TYPE = "gtyp"
    GPS_LATITUDE = "glat"
    GPS_LONGITUDE = "glon"
    GPS_ALTITUDE = "galt"
    GPS_TIME = "gtime"
    BATTERY1_VOLTAGE = "bat1v"
    BATTERY2_VOLTAGE = "bat2v"
    COMPASS_BEARING = "magber"
    CPU_TEMPERATURE = "cputemp"
    WIFI_SIGNAL_STRENGTH = "wifisig"
    RECORDING_STATE = "recstate"
    ALL_DATA = "all"