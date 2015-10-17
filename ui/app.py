#!/usr/bin/env python
# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import platform, tellstick_comm, dbal, tellstick_comm, time, RadioCommunication
from flask import Flask, render_template, request
from datetime import datetime, date
from astral import *
from pytz import timezone

app = Flask(__name__)
db = dbal.DBAL()

@app.route('/')
def index():
	a = Astral()
	gothenburg_latitude = 57.7136505
	gothenburg_longitude =  11.9957975
	location = a
	print date.today()
	print a.sunrise_utc(date.today(), gothenburg_latitude, gothenburg_longitude)
	print a.sunset_utc(date.today(), gothenburg_latitude, gothenburg_longitude)
	sunset_datetime = a.sunset_utc(date.today(), gothenburg_latitude, gothenburg_longitude)
	sunrise_datetime = a.sunrise_utc(date.today(), gothenburg_latitude, gothenburg_longitude)


	sunrise_datetime = sunrise_datetime.astimezone(timezone('Europe/Stockholm'))
	sunset_datetime = sunset_datetime.astimezone(timezone('Europe/Stockholm'))

	return render_template('index.html', devices = db.get_devices(0), 
		events=db.get_events(), temp_sensor_data={}, 
		hum_sensor_data={}, dt=datetime, sunset=sunset_datetime,
		sunrise=sunrise_datetime)

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
	device_id = request.form['light'] #i.light
	mode = request.form['mode'] #i.mode
	r = None
	
	if mode == '1':
		tc.turnOn(device_id)
	else:
		tc.turnOff(device_id)
	return (request.form['light'], r)

@app.route('/add-event', methods=['POST'])
def POST(self):
	
	db.insert_event(request.form['device'], request.form['mode'], 0, 
		datetime(int(request.form['year']), int(request.form['month']), 
			int(request.form['day']), int(request.form['hour']), 
			int(request.form['minute'])))
		
if __name__ == "__main__":
	#application = app.wsgifunc()
	app.debug = True
	app.run(host='0.0.0.0')
