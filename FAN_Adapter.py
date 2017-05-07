import logging
import time
import datetime
from datetime import datetime
form config import HOSTNAME


import RPi.GPIO as GPIO

MODULE_NAME = 'FAN_Adapter'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )

class FAN_Adapter:
        ACTOR_TYPE = 'Fan'
        def __init__(self, gpio, actor_id):
                logging.info(MODULE_NAME+ ": constructor start")
                self.actor_id = actor_id
                self.gpio = gpio
                GPIO.setwarnings(False)#關閉 警告訊息 setwarnings()
                GPIO.setmode(GPIO.BOARD)#設置引腳編號規則 setmode()
                GPIO.setup(gpio, GPIO.OUT) #將gpio號引腳設置成輸出模式 setup()
                self.status = GPIO.input(gpio)#獲取gpio狀態，低電位返回0 / GPIO.LOW / False，高電位返回1 / GPIO.HIGH / True。
                logging.info(MODULE_NAME +": constructor exit")

        def set_on(self):
                GPIO.output(self.gpio, GPIO.HIGH)#將gpio號引腳 狀態設置成高電位 啟動風扇
                self.status = GPIO.input(self.gpio)#獲取gpio狀態
                logging.info(MODULE_NAME+ ": fan on")

        def set_off(self):
                GPIO.output(self.gpio, GPIO.LOW)
                self.status = GPIO.input(self.gpio)#將gpio號引腳 狀態設置成高電位 關閉風扇

                logging.info(MODULE_NAME+ ": fan off")

        def readJSON(self):
                self.status = GPIO.input(self.gpio)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_fan     =    {'hostname':HOSTNAME,
                                'type':self.ACTOR_TYPE,
                                'actorid':self.actor_id,
                                'state':self.status,#紀錄每個引腳狀態
                                'datetime':str(timestamp)}
                return d_fan

