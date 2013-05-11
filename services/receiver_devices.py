# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from ctypes import c_int, c_ubyte, c_void_p, POINTER, string_at #imports allowing the use of our library
from threading import Timer
import time
import platform, sqlite3, dbal, ConfigParser, logging
#platform specific imports:
if (platform.system() == 'Windows'):
	#Windows
	from ctypes import windll, WINFUNCTYPE
	lib = windll.LoadLibrary('TelldusCore.dll') #import our library
else:
	#Linux
	from ctypes import cdll, CFUNCTYPE
	lib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library


config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
config.read(path + '/gcal.cfg')

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename= config.get('General', 'project_path', 0) + 'logs/receiver_devices.log',level=logging.DEBUG)
	
timers = {} #timerlist
db = dbal.DBAL()

       
#function to be called when a device event occurs
# method 1 = on
# method 2 = off
def callbackfunction(deviceId, method, value, callbackId, context):
		global timers, logging

		current_time = time.time()
		if not deviceId in timers or current_time - 0.5 > timers[deviceId]:
			logging.info("Received event for device:" + str(deviceId) + " method: " + method)
			
			status = 1 if method == 1 else 0			
			db.update_device_status(deviceId, status)
			
		timers[deviceId] = current_time

#function to be called when device event occurs, even for unregistered devices
def rawcallbackfunction(data, controllerId, callbackId, context):
	print string_at(data)
if (platform.system() == 'Windows'):
	CMPFUNC = WINFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p) #first is return type
	CMPFUNCRAW = WINFUNCTYPE(None, POINTER(c_ubyte), c_int, c_int, c_void_p)
else:
	CMPFUNC = CFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p)
	CMPFUNCRAW = CFUNCTYPE(None, POINTER(c_ubyte), c_int, c_int, c_void_p)
cmp_func = CMPFUNC(callbackfunction)
cmp_funcraw = CMPFUNCRAW(rawcallbackfunction)
lib.tdInit()
lib.tdRegisterDeviceEvent(cmp_func, 0)
#lib.tdRegisterRawDeviceEvent(cmp_funcraw, 0) #uncomment this, and comment out tdRegisterDeviceEvent, to see data for not registered devices
logging.info("Waiting for events...")
while(1):
	time.sleep(0.5) #don't exit
