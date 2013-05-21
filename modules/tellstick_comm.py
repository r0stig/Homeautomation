# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from ctypes import c_int, c_ubyte, c_void_p, POINTER, string_at #imports allowing the use of our library
import platform, sqlite3, time, dbal

if (platform.system() == 'Windows'):
	#Windows
	from ctypes import windll, WINFUNCTYPE
	lib = windll.LoadLibrary('TelldusCore.dll') #import our library
else:
	#Linux
	from ctypes import cdll, CFUNCTYPE
	lib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library

class tellstick_comm:
	def __init__(self):
		self.dbal = dbal.DBAL()
		
	def turnOn(self, id):
		print "Turning on", id
		lib.tdTurnOn(int(id))
		self.dbal.update_device_status(id, 1)
	
	def turnOff(self, id):
		print "Turning off", id
		lib.tdTurnOff(int(id))
		self.dbal.update_device_status(id, 0)
