Home automation with Telldus Tellstick
======================================

Ever wanted to control your lights with some more logic than simple timers? The rescue is here! With [programname] you will 
control your lights with google calendar! Simple create an event in google calendar and the lights will power on when the event starts 
and off when the event ends. Want your light to power on every day? Create a recurring event!

Installing
==========
Telldus tellstick
-----------------
TODO: Write about installing telldus tellstick
Cronjobs
--------
First make sure services/gcal_fetcher.py and services/event_dispatcher.py is executeable (chmod +x file).
Open crontab with:
> $ crontab -e

Add theese two lines, make sure to change the path to the folder below:
    # Fetch modifications in google calender every day at 12:00
    0 12 * * * /usr/bin/python /path_to/services/gcal_fetcher.py
    # Dispatch events every minute
    */1 * * * * /usr/bin/python /path_to/services/event_dispatcher.py

Services
--------
TODO: Write about running services

Dependencies
============
* Python
* Web.py
* Telldus tellstick

Adding devices
==============
Linux:
/etc/tellstick.conf
Self-learning:
tdtool --learn device

You also need to add the service to the sqlite database:
> insert into devices(device_id, name, type) VALUES(id, name, type);

Device types:
0 - lamp
1 - thermometer sensor
Web interface
=============
Run
> $ python ui/code.py

To start a development server, go to the servers IP port 8080 in the browser (or smartphone).

Upcoming features
=================
* Show temperature graphs for logged temperature data