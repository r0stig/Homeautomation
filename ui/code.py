# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import web, platform, tellstick_comm, dbal, tellstick_comm, time
from datetime import datetime


db = dbal.DBAL()
render = web.template.render('templates/')

urls = (
	'/', 'index',
	'/lights', 'lights',
	'/chart', 'chart',
	'/add-event', 'events'
)


class index:
	
	#tc = tellstick_comm.tellstick_comm()
	def GET(self):
		#i = web.input(name=None)
		#print self.tc.getDevices()
		return render.index( {'devices': db.get_devices(0), 'events': db.get_events(),
			'temp_sensor_data' : db.get_last_sensor_data(), 'hum_sensor_data': db.get_last_sensor_data(1)
			, 'dt': datetime})
			#render.index
		
class chart:
	def GET(self):
		i = web.input()
		print i
		start = None
		end = None
		if 'start' in i:
			start = time.strptime(i.start, "%Y-%m-%dT%H:%M")
		if 'end' in i:
			end = time.strptime(i.end, "%Y-%m-%dT%H:%M")
		
		return render.chart( {'sensor_data': db.get_sensor_data_for(90, 0, start, end), 'dt': datetime } )
		
		
class lights:
	tc = tellstick_comm.tellstick_comm()
	def POST(self):
		i = web.input()
		device_id = i.light
		mode = i.mode
		r = None
		
		if mode == '1':
			self.tc.turnOn(device_id)
		else:
			self.tc.turnOff(device_id)

		return (i.light, r)
		#raise web.seeother('/')
		
class events:
	def POST(self):
		i = web.input()
		
		db.insert_event(i.device, i.mode, 0, datetime(int(i.year), int(i.month), int(i.day), int(i.hour), int(i.minute)))
		
		#raise web.seeother('/#events')
		
		
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
	