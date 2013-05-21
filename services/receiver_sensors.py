# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from ctypes import c_int, c_ubyte, c_void_p, POINTER, string_at, create_string_buffer, c_char_p, c_int, byref #imports allowing the use of our library
import time, platform, sqlite3, dbal
from datetime import datetime
#platform specific imports:
if (platform.system() == 'Windows'):
	#Windows
	from ctypes import windll, WINFUNCTYPE
	lib = windll.LoadLibrary('TelldusCore.dll') #import our library
else:
	#Linux
	from ctypes import cdll, CFUNCTYPE
	lib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library
TELLSTICK_TEMPERATURE = 1;
TELLSTICK_HUMIDITY = 2;

#function to be called when a sensor event occurs               
def callbackfunction(protocol, model, id, dataType, value, timestamp, callbackId, context):
	db = dbal.DBAL()
	print "Sensor:", string_at(protocol), string_at(model), "id:", id
	if(dataType == TELLSTICK_TEMPERATURE):
		print "Temperature:", string_at(value), "C,", datetime.fromtimestamp(timestamp)
		temp = float(string_at(value))
		db.insert_sensor_data(id, temp)


	elif(dataType == TELLSTICK_HUMIDITY):
		print "Humidity:", string_at(value), "%,", datetime.fromtimestamp(timestamp)
		hum = int(string_at(value))
	print ""
		

if (platform.system() == 'Windows'):
	CMPFUNC = WINFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte), c_int, c_int, POINTER(c_ubyte), c_int, c_int, c_void_p) #first is return type
else:
	CMPFUNC = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte), c_int, c_int, POINTER(c_ubyte), c_int, c_int, c_void_p)
cmp_func = CMPFUNC(callbackfunction)
lib.tdInit()
callbackid = lib.tdRegisterSensorEvent(cmp_func, 0)
print "Waiting for events..."
try:
	while(1):
		time.sleep(0.5) #don't exit
except KeyboardInterrupt:
	print "Exiting"
	lib.tdUnregisterCallback(callbackid)
	lib.tdClose()
