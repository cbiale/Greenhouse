#!/usr/bin/python
# Copyright (c) 2016 
# Author: Andreas Wirthmueller
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import logging
import time
import datetime
from datetime import datetime
from config import HOSTNAME
import smbus


MODULE_NAME = 'BH1750_Adapter'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )

class BH1750_Adapter:
        SENSOR_TYPE = "luminosity"
        #MEASURE_L="lux"
        DEVICE     = 0x23
        POWER_DOWN = 0x00
        POWER_ON   = 0x01 # Power on
        RESET      = 0x07 # Reset data register value
        ONE_TIME_HIGH_RES_MODE_1 = 0x20
        def __init__(self, sensor_id):
                logging.info(MODULE_NAME+ ": constructor start")
                self.bus = smbus.SMBus(1)
                self.sensor_id = sensor_id
                logging.info(MODULE_NAME +": constructor exit")
        def read(self):
                lux = str(self.readLight())
                return lux
        def convertToNumber(self, data):
                return ((data[1] + (256 * data[0])) / 1.2)
        def readLight(self):
                data = self.bus.read_i2c_block_data(self.DEVICE,self.ONE_TIME_HIGH_RES_MODE_1)
                return  self.convertToNumber(data)
        def readJSON(self):
                lux = self.read()
                logging.info(MODULE_NAME+ ": luminosity="+lux)
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                d_luminosity = 	{'hostname':HOSTNAME,
             			         'type':self.SENSOR_TYPE,
             			         'sensorid':self.sensor_id,
             			         'luminosity':lux,
             			         'datetime':str(timestamp)}
		return d_luminosity
	
