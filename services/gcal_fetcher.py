#!/usr/bin/python
# Append module path
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import dbal
import gflags
import httplib2
import logging

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from dbal import DBAL
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz, string
import ConfigParser

config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
config.read(path + '/gcal.cfg')

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', filename= config.get('General', 'project_path', 0) + 'logs/gcal_fetcher.log',level=logging.DEBUG)


FLAGS = gflags.FLAGS

"""
Source: https://developers.google.com/google-apps/calendar/v3/reference/events/insert
"""

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
	client_id= config.get('Google calendar', 'client_id', 0) ,
	client_secret=config.get('Google calendar', 'client_secret', 0),
	scope='https://www.googleapis.com/auth/calendar',
	user_agent=config.get('Google calendar', 'user_agent', 0))

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
storage = Storage(path + '/calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
	credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
	developerKey=config.get('Google calendar', 'api_key', 0))



class GCALFetcher():
	def __init__(self, calID = config.get('Google calendar', 'calendar_id', 0)):
		self.calID = calID
		self.dbal = dbal.DBAL()
		
	def fetch(self):
		global logging
		""" Fetches events from the event calendar """
		
		self.dbal.remove_auto_events()
		# Fetch events for just one day because of the update time
		min = datetime.today()
		max = datetime.today() + timedelta(days = 1)
		min = min.replace(tzinfo = timezone('Europe/Stockholm'))
		max = max.replace(tzinfo = timezone('Europe/Stockholm'))
		#localtz = dateutil.tz.tzlocal()

		events = service.events().list(calendarId= self.calID, singleEvents = True, timeMin = str(min).replace(' ', 'T'), timeMax = str(max).replace(' ', 'T')).execute()
		if events['items']:
			#print "NUMER IF ITEMS:", len(events['items'])
			logging.info('Found ' + str(len(events['items'])) + ' events, inserting in database..')
			for event in events['items']:
				# format: readable name:deviceId
				tmp = string.split(event['summary'], ':')
				if len(tmp) < 2:
					continue
				name = tmp[0]
				id = tmp[1]
				
				# Insert two entries, one for device ON one for device OFF
				start = event['start']['dateTime'][0:string.find(event['start']['dateTime'], '+')]
				start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
				
				end = event['end']['dateTime'][0:string.find(event['end']['dateTime'], '+')]
				end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
				
				# Adjust to UTC
				#utcplus = event['start']['dateTime'][string.find(event['start']['dateTime'], '+')+1:]
				#utcplushours = utcplus[0:string.find(utcplus, ':')]
				#utcplusminutes = utcplus[string.find(utcplus, ':')+1:]
				
				#start = start - timedelta(hours=int(utcplushours), minutes=int(utcplusminutes))
				#end = end -  timedelta(hours=int(utcplushours), minutes=int(utcplusminutes))
				
				
				
				if start > datetime.today():
					self.dbal.insert_event(id, 1, 1, start)
				
				if end > datetime.today():
					self.dbal.insert_event(id, 0, 1, end)
				

	#calendar = service.calendars().get(calendarId='tho6sjnta0mmpf8kvjsc93fkvs@group.calendar.google.com').execute()

#print calendar['summary']
#print calendar

logging.info('Starting fetcher')
f = GCALFetcher()
f.fetch()