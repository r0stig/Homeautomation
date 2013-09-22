#!/usr/bin/env python
# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import platform, tellstick_comm, dbal, tellstick_comm, time, RadioCommunication
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
application = app
db = dbal.DBAL()

urls = (
	'/', 'index',
	'/lights', 'lights',
	'/chart', 'chart',
	'/add-event', 'events'
)

@app.route('/')
def index():
	return render_template('index.html', devices = db.get_devices(0), events={}, temp_sensor_data={}, hum_sensor_data={}, dt=datetime)

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

@app.route('/lights', methods=['POST'])	
def lights():
	tc = RadioCommunication.RadioCommunication() #tellstick_comm.tellstick_comm()
	#i = web.input()
	device_id = request.form['light'] #i.light
	mode = request.form['mode'] #i.mode
	r = None
	
	if mode == '1':
		tc.turnOn(device_id)
	else:
		tc.turnOff(device_id)
	return (request.form['light'], r)
	#return (i.light, r)
	#raise web.seeother('/')
		
class events:
	def POST(self):
		i = web.input()
		
		db.insert_event(i.device, i.mode, 0, datetime(int(i.year), int(i.month), int(i.day), int(i.hour), int(i.minute)))
		
		#raise web.seeother('/#events')

# uWSGI dosen't run in the __name__ == "__main__", therefore theese lays here:

#app = web.application(urls, globals())
#application = app.wsgifunc()
		
if __name__ == "__main__":
	#application = app.wsgifunc()
	app.debug = True
	app.run(host='0.0.0.0')
