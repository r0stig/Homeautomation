#!/usr/bin/python
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

import dbal, SunPosition


db = dbal.DBAL()
events = db.get_recurring_events()

for e in events:
    print e
    if e['sunrise'] == 1:
        print 'is sunrise'
        sunrise = SunPosition.get_today_sunrise()
        db.insert_event(e['device_id'], e['type'], e['auto'], sunrise)
    elif e['sunset'] == 1:
        print 'is sunset'
        sunset = SunPosition.get_today_sunset()
        db.insert_event(e['device_id'], e['type'], e['auto'], sunset)