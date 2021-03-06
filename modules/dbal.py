import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import sqlite3, calendar, time, ConfigParser, os, sys, calendar, SunPosition
from datetime import timedelta, datetime

config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
config.read(path + '/gcal.cfg')

class DBAL():
	def __init__(self):
		self.conn = sqlite3.connect(config.get('General', 'database_path', 0), check_same_thread=False)
		self.conn.row_factory = sqlite3.Row
		
	def remove_auto_events(self):
		cursor = self.conn.cursor()
		with self.conn:
			cursor.execute('DELETE FROM events WHERE auto = 1')
		cursor.close()
		
	def insert_event(self, deviceId, type, auto, fire_at, sunset=0, sunrise=0, mo=0, tu=0, we=0, th=0, fr=0, sa=0, su=0):
		cursor = self.conn.cursor()
		with self.conn:
			cursor.execute('INSERT INTO events(device_id, type, fire_at, auto, sunset, sunrise, mo, tu, we, th, fr, sa, su)' + 
				' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
				(deviceId, type, int(fire_at.strftime('%s')) , auto, sunset, sunrise, mo, tu, we, th, fr, sa, su))
		cursor.close()
		#calendar.timegm(fire_at.utctimetuple())
		
	def insert_sensor_data(self, deviceId, value, when, type = 0):
		cursor = self.conn.cursor()
		with self.conn:
			cursor.execute('INSERT INTO sensor_data(device_id, value, timestamp, type) VALUES(?, ?, ?, ?)', 
				(deviceId, value, calendar.timegm(when.timetuple()), type)) # datetime.today().strftime('%s') calendar.timegm(datetime.today().timetuple())
		cursor.close()
		
	def get_last_sensor_data(self, type = 0):
		cursor = self.conn.cursor()
		
		res = cursor.execute('SELECT sensor_data.value, sensor_data.timestamp, devices.name, devices.type ' + 
			'FROM sensor_data INNER JOIN devices ON sensor_data.device_id = devices.device_id ' + 
			'WHERE sensor_data.type = ? ' + 
			'GROUP BY sensor_data.device_id ORDER BY sensor_data.timestamp DESC', (type,))
		rows = res.fetchall()
		cursor.close()
		return rows
		
	def get_sensor_data_for(self, deviceId, type = 0, start = None, end = None):
		cursor = self.conn.cursor()
		
		params = (type,)
		whereAppend = None
		if start is not None:
			whereAppend = 'AND sensor_data.timestamp > ? '
			params = params + (calendar.timegm(start),)
		if end is not None:
			whereAppend = whereAppend + ' AND sensor_data.timestamp < ? '
			params = params + (calendar.timegm(end),)
			
		sql = 'SELECT sensor_data.value, sensor_data.timestamp, devices.name, devices.type FROM sensor_data INNER JOIN devices ON sensor_data.device_id = devices.device_id '
		sql = sql + ' WHERE sensor_data.type = ? '
		if whereAppend is not None:
			sql = sql + whereAppend
		sql = sql + 'ORDER BY sensor_data.timestamp ASC'
		
		print sql
		print whereAppend
		print params
		res = cursor.execute(sql, params)#((datetime.today() - timedelta(hours=1)).strftime('%s'),))
		rows = res.fetchall()
		cursor.close()
		return rows
		
	def get_events(self):
		cursor = self.conn.cursor()
		res = cursor.execute('SELECT events.device_id, events.auto, events.type, events.fire_at, events.sunrise, events.sunset, ' +
			'events.mo, events.tu, events.we, events.tu, events.fr, events.sa, events.su, ' +  
			' devices.name, devices.type FROM events INNER JOIN devices ON devices.device_id = events.device_id ORDER BY events.fire_at ASC')
		rows = res.fetchall()
		cursor.close()
		return rows
	
	def pop_event(self):
		""" Pops one event to dispatch and deletes it from the database """
		cursor = self.conn.cursor()
		res = cursor.execute('''SELECT events.id, events.device_id, events.auto, events.type, events.fire_at, devices.name, devices.type 
			FROM events INNER JOIN devices ON devices.device_id = events.device_id WHERE 
			(events.mo = 0 and events.tu = 0 and events.we = 0 and events.tu = 0 and events.fr = 0 and events.sa = 0 and events.su = 0) 
			AND events.fire_at <= ?''', (time.time(),))
		event = res.fetchone()
		if event is not None:
			with self.conn:
				cursor.execute('DELETE FROM events WHERE id = ?', (event[0],))
		cursor.close()
		return event

	def get_recurring_events(self):
		""" Gets recurring events that should be dispatched.. """
		cursor = self.conn.cursor()

		sql = '''SELECT events.id, events.device_id, events.auto, events.type, events.sunrise, events.sunset FROM events  
			WHERE (events.sunrise = 1 or events.sunset = 1) '''
		# INNER JOIN devices ON devices.device_id = events.device_id
		whereAppend = ""
		wd = datetime.today().weekday()
		whereAppend = whereAppend + ' AND ' + self.get_column_from_weekday(wd) + ' = 1'

		sql = sql + whereAppend

		res = cursor.execute(sql)
		rows = res.fetchall()
		cursor.close()
		return rows


	def get_column_from_weekday(self, wk):
		if wk == 0:
			return 'mo'
		elif wk == 1:
			return 'tu'
		elif wk == 2:
			return 'we'
		elif wk == 3:
			return 'th'
		elif wk == 4:
			return 'fr'
		elif wk == 5:
			return 'sa'
		elif wk == 6:
			return 'su'
		return 'none'


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
