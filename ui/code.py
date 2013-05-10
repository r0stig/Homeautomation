# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import web, platform, tellstick_comm, dbal, tellstick_comm
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
		return render.index( {'devices': db.get_devices(), 'events': db.get_events(), 'dt': datetime})
			#render.index
		
class chart:
	def GET(self):
		return render.chart()
		
		
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
	