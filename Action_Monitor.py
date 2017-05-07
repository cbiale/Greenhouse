#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Copyright (c) 2016 Andreas Wirthmueller
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
#監視檔

import rethinkdb as r
import time
import datetime
import sys
import json
from datetime import datetime



MODULE_NAME = 'Action_Monitor'
TABLE_NAME = 'action_triggers'
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='/home/pi/GreenMon/log/adapter_log.log'
    )

from FAN_Adapter import FAN_Adapter


class Action_Monitor:
	
	def __init__(self):
		self.initDB()		

	def initDB(self):
		conn = r.connect('10.74.23.153', db='irving',port='28015')
		#conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
		#logging.info(MODULE_NAME+": Successful DB connection")

		#logging.info(MODULE_NAME+": Checking if db %s exists",DB_NAME)
		#if DB_NAME not in list(r.db_list().run(conn)):
    			#logging.info(MODULE_NAME+": db does not exist, creating...")
    			#r.db_create(DB_NAME).run(conn)
		#logging.info(MODULE_NAME+": db exists")

		#logging.info(MODULE_NAME+": Checking to see if table %s exists",TABLE_NAME)
		#if TABLE_NAME  not in list(r.table_list().run(conn)):
    			#logging.info(MODULE_NAME+": table does not exist, creating...")
    			#r.table_create(TABLE_NAME).run(conn)
		#logging.info(MODULE_NAME+": table exists")
		conn.close()
     #監控清理方法
	def monitorCleanup(self):
                logging.info(MODULE_NAME+"::trying to open database")
                conn = r.connect('10.74.23.153', db='irving',port='28015')
		try:#異常監控用
			#delete all pending entries
			r.table(TABLE_NAME).filter(r.row['action_state'] == 'pending').delete().run(conn)
			conn.close() 
                except:#異常代碼的處理
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        logging.error(MODULE_NAME+"::exception %s %s %s",exc_type, exc_value, exc_traceback)
                        conn.close() 
    #監控操做
	def monitorAction(self):
		logging.info(MODULE_NAME+"::trying to open database")
                conn = r.connect(DB_HOST, DB_PORT, DB_NAME)
              
		try:
			logging.info(MODULE_NAME+"::entering watch loop")
			while True:
				logging.info(MODULE_NAME+"::yielding")#include_types=True 紀錄TYPE    #include_initial=False 紀錄old_val 跟new_val
                		feed = r.table(TABLE_NAME).changes(include_initial=False,include_types=True).run(conn)
                              	for document in feed:
					logging.info(MODULE_NAME+":: received change type:" + str(document['type']))#紀錄type,add, remove, change, initial, uninitial, state
					if document['type'] == 'add':
    						logging.info(MODULE_NAME+":: received document:" + str(document['new_val']))#紀錄收到的文件

						# do some stuff with the action parameters now
						actorid = document['new_val']['actorid']# {new_val{actorid}} 存'actorid'到actorid
						actortype = document['new_val']['type']
						actiontype = document['new_val']['actiontype']
						actionvalue = document['new_val']['actionvalue']
						self.executeAction(actorid,actortype,actiontype,actionvalue)

						# update table with execution status   更新表的執行狀態
						timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						r.table(TABLE_NAME).filter(r.row['id'] == document['new_val']['id']).update({"action_state": "done","action_timestamp":timestamp}).run(conn)
                        #查詢表單欄位id是否跟監視的id一樣 並更新時間與狀態

		except:
            		exc_type, exc_value, exc_traceback = sys.exc_info()
            		logging.error(MODULE_NAME+"::exception %s %s %s",exc_type, exc_value, exc_traceback)
			conn.close() 
           		
	def executeAction(self,actorid,actortype,actiontype,actionvalue):
		logging.info(MODULE_NAME+"::starting action execution ("+actorid+','+actortype+','+actiontype+','+actionvalue+')')
		conn = r.connect(DB_HOST, DB_PORT, DB_NAME)

		if   == 'f_0001':
			 logging.info(MODULE_NAME+"::action for " + actortype + " with id " + actorid + "identified")
			 fan = FAN_Adapter(16,'f_0001')
			 if actionvalue == 'On':
				fan.set_on()
				d_fan = fan.readJSON()
				d_observation = {'fan':[d_fan],
                 				 'timestamp': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                 				 'type':'actors'
                				}

				r.table("observations").insert(d_observation).run(conn, durability='soft') 
				logging.info(MODULE_NAME+"::action fan on for " + actortype + " with id " + actorid + " executed")

			 elif actionvalue == 'Off':
				fan.set_off()
				d_fan = fan.readJSON()
				d_observation = {'fan':[d_fan],
                                                 'timestamp': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                                 'type':'actors'
                                                }
				r.table("observations").insert(d_observation).run(conn, durability='soft')
				logging.info(MODULE_NAME+"::action fan off for " + actortype + " with id " + actorid + " executed")  

		conn.close()
		logging.info(MODULE_NAME+"::ending action execution")
		
			
