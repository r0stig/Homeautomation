import sqlite3, calendar, time, ConfigParser, os, sys
from datetime import timedelta, datetime

config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
config.read(path + '/gcal.cfg')

class DBAL():
	def __init__(self):
		self.conn = sqlite3.connect(config.get('General', 'database_path', 0), check_same_thread=False)
		
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
		
	def insert_sensor_data(self, deviceId, value):
		cursor = self.conn.cursor()
		with self.conn:
			cursor.execute('INSERT INTO sensor_data(device_id, value, timestamp) VALUES(?, ?, ?)', 
				(deviceId, value, datetime.today().strftime('%s')))
		cursor.close()
		
	def get_last_sensor_data(self):
		cursor = self.conn.cursor()
		
		res = cursor.execute('SELECT sensor_data.value, sensor_data.timestamp, devices.name, devices.type ' + 
			'FROM sensor_data INNER JOIN devices ON sensor_data.device_id = devices.device_id ' + 
			'GROUP BY sensor_data.device_id ORDER BY sensor_data.timestamp DESC')
		rows = res.fetchall()
		cursor.close()
		return rows
		
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

	def get_devices(self, type = None):
		cursor = self.conn.cursor()
		if type is not None:
			res = cursor.execute('SELECT devices.device_id, devices.name, devices.type, device_status.status FROM devices LEFT JOIN device_status ON device_status.device_id = devices.device_id WHERE devices.type = ?', (type,))
		else:
			res = cursor.execute('SELECT devices.device_id, devices.name, devices.type, device_status.status FROM devices LEFT JOIN device_status ON device_status.device_id = devices.device_id')
		rows = res.fetchall()
		cursor.close()
		return rows
		
	def get_device(self, deviceId):
		cursor = self.conn.cursor()
		res = cursor.execute('SELECT devices.device_id, devices.name, devices.type, device_status.status FROM devices ' + 
			'LEFT JOIN device_status ON device_status.device_id = devices.device_id ' + 
			'WHERE devices.device_id = ?', (deviceId,))
		row = res.fetchone()
		cursor.close()
		return row
		
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
