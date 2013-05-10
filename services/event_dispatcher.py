#!/usr/bin/python
# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import dbal, tellstick_comm, time

class EventDispatcher():
	def __init__(self):
		self.db = dbal.DBAL()
		self.tc = tellstick_comm.tellstick_comm()
		
	def poll(self):
		""" Poll for events to dispatch """
		event = self.db.pop_event()
		while event is not None:
			event[3]
			if event[3] == 0: # Lamp off
				print "Turning device", event[1], "OFF"
				self.tc.turnOff(int(event[1]))
			elif event[3] == 1: # Lamp on
				print "Turning device", event[1], "ON"
				self.tc.turnOn(int(event[1]))
			
			event = self.db.pop_event()

if __name__ == "__main__":
	e = EventDispatcher()
	print "Starting..."
	e.poll()
	
	# If no cronjob, forever loop
	#try:
	#	while True:
	#		e.poll()
	#		time.sleep(60)
	#except KeyboardInterrupt:
	#	print "...Exiting"
