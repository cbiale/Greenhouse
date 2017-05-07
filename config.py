import RPi.GPIO as GPIO
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket

HOSTNAME = socket.gethostname()

DB_HOST =""
#在Class  A之中，有4個網域無法使用，分別為0.0.0.0/8、
#10.0.0.0/8、100.64.0.0/10、127.0.0.0/8。0.0.0.0/8
#是個特殊的網路區段，這個位址表示所有、任何、預設的意思。
#如果在路由表的來源IP為只填入0.0.0.0，代表的就是無論資料封包從哪裡過來
#一律套用此路由規則。
DB_PORT = 28015
DB_NAME = ""
PROJECT_TABLE = ''
