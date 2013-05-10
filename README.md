Home automation with Telldus Tellstick

Ever wanted to control your lights with some more logic than simple timers? The rescue is here! With [programname] you will 
control your lights with google calendar! Simple create an event in google calendar and the lights will power on when the event starts 
and off when the event ends. Want your light to power on every day? Create a recurring event!

Installing
==========
* Telldus tellstick
* Cronjobs
* Services

Dependencies
============
* Web.py
* Telldus tellstick
* 

Adding devices
==============
Linux:
/etc/tellstick.conf
Self-learning:
tdtool --learn device
Web interface
=============
Run
> $ python ui/code.py
To start a development server, go to the servers IP port 8080 in the browser (or smartphone).

Cronjobs:
Fetch modifications in google calender every day at 12:00
0 12 * * * /usr/bin/python /home/robert/tellstick/services/gcal_fetcher.py
Dispatch events every other second
*/1 * * * * /usr/bin/python /home/robert/tellstick/services/event_dispatcher.py

Info abt cronjob and python..
http://stackoverflow.com/questions/4460262/running-a-python-script-with-cron