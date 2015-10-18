#!/usr/bin/env python
# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import platform, tellstick_comm, dbal, tellstick_comm, time, RadioCommunication, SunPosition
from flask import Flask, render_template, request
from datetime import datetime, date
from pytz import timezone

app = Flask(__name__)
db = dbal.DBAL()

@app.route('/')
def index():
	return render_template('index.html', devices = db.get_devices(0), 
		events=db.get_events(), temp_sensor_data={}, 
		hum_sensor_data={}, dt=datetime, sunset=SunPosition.get_today_sunset(),
		sunrise=SunPosition.get_today_sunrise())

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
	# Development
	#tc = RadioCommunication.RadioCommunication() #tellstick_comm.tellstick_comm()
	# Production	
	tc = tellstick_comm.tellstick_comm();
	device_id = request.form['light'] #i.light
	mode = request.form['mode'] #i.mode
	r = None
	
	if mode == '1':
		tc.turnOn(device_id)
	else:
		tc.turnOff(device_id)
	return (request.form['light'], r)

@app.route('/add-event', methods=['POST'])
def POST():
	
	db.insert_event(request.form['device'], request.form['mode'], 0, 
		datetime(
			int(request.form['year']), 
			int(request.form['month']), 
			int(request.form['day']), 
			int(request.form['hour']), 
			int(request.form['minute'])), 
			'sunset' in request.form, 
			'sunrise' in request.form,
			'mo' in request.form,
			'tu' in request.form,
			'we' in request.form,
			'th' in request.form,
			'fr' in request.form,
			'sa' in request.form,
			'su' in request.form)
		
if __name__ == "__main__":
	#application = app.wsgifunc()
	app.debug = True
	app.run(host='0.0.0.0')
