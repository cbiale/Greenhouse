#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THE SOFTWARE.
import rethinkdb as r
import time
import datetime
import sys
from datetime import datetime
from config import HOSTNAME, DB_HOST, DB_PORT, DB_NAME
#from BMP_adapter import BMP_Adapter
from DS18B20_adapter import DS18B20_Adapter
from Sunrise_Adapter import Sunrise_Adapter
from  BH1750_adapter import  BH1750_Adapter
from  DHT22_adapter import  DHT22_Adapter

MODULE_NAME = 'monitor_adapters'
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )
logging.info(MODULE_NAME+": ***************** Start ***************** ")

conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
logging.info(MODULE_NAME+": Successful DB connection")

logging.info(MODULE_NAME+": Checking if db %s exists",DB_NAME)
if DB_NAME not in list(r.db_list().run(conn)):
    logging.info(MODULE_NAME+"db does not exist, creating...")
    r.db_create(DB_NAME).run(conn)
logging.info(MODULE_NAME+": db exists")

logging.info(MODULE_NAME+": Checking to see if table %s exists",'observations')
if 'observations' not in list(r.table_list().run(conn)):
    logging.info(MODULE_NAME+": table does not exist, creating...")
    r.table_create("observations").run(conn)
logging.info(MODULE_NAME+": table exists")

timezone = time.strftime("%z")
reql_tz = r.make_timezone(timezone[:3] + ":" + timezone[3:])

# measure pressure
#bmp = BMP_Adapter(350,'p_0001')

#d_pressure = bmp.readJSON()

#print(d_pressure)

#measure temperature sensor 1
soil_temperature = DS18B20_Adapter('t_0001','28-000007a5d7a0')
d_temp1 =  soil_temperature.readJSON()
print(d_temp1)

#measure temperature sensor 2
outside_temperature = DS18B20_Adapter('t_0002','28-041636dddaff')
d_temp2 =  outside_temperature.readJSON()
print(d_temp2)

lumen_sensor =  BH1750_Adapter('lx_0001')
d_luminosity = lumen_sensor.readJSON()
print(d_luminosity)

#get sunrise and sunset forcast
sunforcast = Sunrise_Adapter('s_0001','23.951545','120.929693')
d_sun = sunforcast.readJSON()
print(d_sun)

#get humidity temperature DHT22 sensor 1
DHT22_sensor =  DHT22_Adapter('DHT_0001')
d_hum = DHT22_sensor.readJSON()
print(d_hum)

d_observation = {#'pressure':[d_pressure],
                 'temperature':[d_temp1,d_temp2],
                 'luminosity':[d_luminosity],
                 'humidity':[d_hum],
                 'timestamp': str(datetime.now(reql_tz)),
                 'type':'sensors'
                }

d_sunset = {'sunset':[d_sun],
            'timestamp': str(datetime.now(reql_tz)),
            'type':'sunset'
           }
logging.info(MODULE_NAME+": measurement %s",str(d_observation))
print(d_observation)
r.table("observations").insert(d_observation).run(conn, durability='soft') #Soft durability since losing one observation wouldn't be the end of the world.
r.table("observations").insert(d_sunset).run(conn, durability='soft')
conn.close()
print("end")
logging.info(MODULE_NAME+": measurements successfully written to db")
logging.info(MODULE_NAME+": ***************** End ***************** ")
