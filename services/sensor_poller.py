#!/usr/bin/python
# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
from ctypes import c_int, c_ubyte, c_void_p, POINTER, string_at, create_string_buffer, c_char_p, c_int, byref #imports allowing the use of our library
from threading import Timer
import time
import platform
import dbal
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
def poll():
	db = dbal.DBAL()
	print "getting sensors"

	protocollength = 20
	modellength = 20
	valuelength = 20

	protocol = create_string_buffer(protocollength)
	model = create_string_buffer(modellength)
	idvalue = c_int()
	dataTypes = c_int()
	while(lib.tdSensor(protocol, protocollength, model, modellength, byref(idvalue), byref(dataTypes)) == 0):
		print "Sensor: ", protocol.value, model.value, "id:", idvalue.value
		value = create_string_buffer(valuelength)
		timestampvalue = c_int()

		if((dataTypes.value & TELLSTICK_TEMPERATURE) != 0):
			success = lib.tdSensorValue(protocol.value, model.value, idvalue.value, TELLSTICK_TEMPERATURE, value, valuelength, byref(timestampvalue))
			print "Temperature: ", value.value, "C,", datetime.fromtimestamp(timestampvalue.value)
			
			device = db.get_device(int(idvalue.value))
			# type 1 = thermometer, type 2 = thermometer and humidity, both catches degrees
			if device is not None and (device[2] == 1 or device[2] == 2):
				db.insert_sensor_data(int(idvalue.value), value.value, datetime.fromtimestamp(timestampvalue.value), 0)

		if((dataTypes.value & TELLSTICK_HUMIDITY) != 0):
			success = lib.tdSensorValue(protocol.value, model.value, idvalue.value, TELLSTICK_HUMIDITY, value, valuelength, byref(timestampvalue))
			print "Humidity: ", value.value, "%,", datetime.fromtimestamp(timestampvalue.value)
			
			device = db.get_device(int(idvalue.value))
			#  type 2 = thermometer and humidity
			if device is not None and device[2] == 2:
				db.insert_sensor_data(int(idvalue.value), value.value, datetime.fromtimestamp(timestampvalue.value), 1)

	print " "
lib.tdInit()
poll()
lib.tdClose()
