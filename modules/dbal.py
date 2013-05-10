import sqlite3, calendar, time
from datetime import timedelta

class DBAL():
	def __init__(self):
		self.conn = sqlite3.connect('/home/robert/tellstick/db/temp.db', check_same_thread=False)
		
	def remove_auto_events(self):
		cursor = self.conn.cursor()
		with self.conn:
			cursor.execute('DELETE FROM events WHERE auto = 1')
		cursor.close()
		
	def insert_event(self, deviceId, type, auto, fire_at):
		cursor = self.conn.cursor()
		with self.conn:
			cursor.execute('INSERT INTO events(device_id, type, fire_at, auto) VALUES(?, ?, ?, ?)', 
				(deviceId, type, int(fire_at.strftime('%s')) , auto))
		cursor.close()
		#calendar.timegm(fire_at.utctimetuple())
		
	def get_events(self):
		cursor = self.conn.cursor()
		res = cursor.execute('SELECT events.device_id, events.auto, events.type, events.fire_at, devices.name, devices.type FROM events INNER JOIN devices ON devices.device_id = events.device_id ORDER BY events.fire_at ASC')
		rows = res.fetchall()
		cursor.close()
		return rows
	
	def pop_event(self):
		""" Pops one event to dispatch and deletes it from the database """
		cursor = self.conn.cursor()
		res = cursor.execute('SELECT events.id, events.device_id, events.auto, events.type, events.fire_at, devices.name, devices.type FROM events INNER JOIN devices ON devices.device_id = events.device_id WHERE events.fire_at <= ?', (time.time(),))
		event = res.fetchone()
		if event is not None:
			with self.conn:
				cursor.execute('DELETE FROM events WHERE id = ?', (event[0],))
		cursor.close()
		return event

	def get_devices(self):
		cursor = self.conn.cursor()
		res = cursor.execute('SELECT devices.device_id, devices.name, devices.type, device_status.status FROM devices LEFT JOIN device_status ON device_status.device_id = devices.device_id')
		rows = res.fetchall()
		cursor.close()
		return rows
		
	def update_device_status(self, deviceId, status):
		cursor = self.conn.cursor()
		current_time = time.time()
		cursor.execute('SELECT COUNT(device_id) FROM device_status WHERE device_id = ?', ( deviceId, ))
		row = cursor.fetchone()
		print "eyyaa", row
		with self.conn:
			if row[0] > 0:
				cursor.execute('UPDATE device_status SET status = ?, last_update = ? WHERE device_id = ?', (status, current_time, deviceId))
			else:
				cursor.execute('INSERT INTO device_status(device_id, status, last_update) VALUES(?, ?, ?)', (deviceId, status, current_time))
		cursor.close()
