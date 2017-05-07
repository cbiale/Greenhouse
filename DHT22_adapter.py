import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime
import Adafruit_DHT
import logging
from config import HOSTNAME

MODULE_NAME = 'DHT22'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )


class DHT22_Adapter:
        SENSOR_TYPE = "humidity and temperature"
        def __init__(self, sensor_id):
                logging.info(MODULE_NAME+ ": constructor start")
                self.sensor_id = sensor_id
                logging.info(MODULE_NAME +": constructor exit")


        def read(self):
                Hum, Temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 24)
                return (str(Hum), str(Temp))

        def readJSON(self):
                Hum, Temp = self.read()
                logging.info(MODULE_NAME +": humidity="+Hum+" temperature="+Temp)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_hum =        {'hostname':HOSTNAME,
                                'type':self.SENSOR_TYPE,
                                "temp": Temp,
                                'sensorid':self.sensor_id,
                                'hum':Hum,
                                'datetime':str(timestamp)}
                return d_hum
