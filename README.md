Home automation with Telldus Tellstick
======================================

Ever wanted to control your lights with some more logic than simple timers? The rescue is here! With [programname] you will 
control your lights with google calendar! Simple create an event in google calendar and the lights will power on when the event starts 
and off when the event ends. Want your light to power on every day? Create a recurring event!

Installing
==========
Telldus tellstick
-----------------
To install the tellstick using debian/ubuntu, follow this guide:
http://developer.telldus.com/wiki/TellStickInstallationUbuntu

To install the tellstick on Raspberry PI with Raspbian, follow the following instructions:
http://www.telldus.com/forum/viewtopic.php?p=13857#p13857

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
	# Poll sensor data every 10 minutes
	*/10 * * * * /usr/bin/python /path_to/services/sensor_poller.py

Services
--------
TODO: Write about running services

Dependencies
============
* Python
* Flask
* Telldus tellstick
* Pytz
* google-api-python-client: https://developers.google.com/google-apps/calendar/setup

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
2 - thermometer and humidity sensor
Web interface
=============
Run
> $ python ui/app.py

To start a development server, go to the servers IP port 5000 in the browser (or smartphone).


Using Nginx on Ubuntu (or other debian-based dist)
--------------------------------------------------
sudo apt-get install nginx-full uwsgi uwsgi-plugin-python

File /etc/nginx/sites-enabled/default:
server {
        listen 3000;

        root /path_to_project/ui;
        index index.html index.htm;

        server_name 0.0.0.0;
        access_log /var/log/nginx/default_access.log;
        error_log /var/log/nginx/default_error.log;

        location / {
                include uwsgi_params;

                uwsgi_pass unix://tmp/uwsgi_vhosts.sock;
                uwsgi_param UWSGI_CHDIR /path_to_project/ui;
                uwsgi_param UWSGI_PYHOME /path_to_project/ui;
                uwsgi_param UWSGI_SCRIPT code;
        }

        location /static {
                alias /path_to_project/ui/static;
        }
}

File /etc/uwsgi/apps-enabled/vhosts.ini
[uwsgi]
plugins = python
gid = www-data
uid = www-data
vhost = true
logdate
socket = /tmp/uwsgi_vhosts.sock
master = true
processes = 1
harakiri = 20
limit-as = 128
memory-report
no-orphans

Permissions:
* code.py should be executeable by www-data
* db/ and db/temp.db should be read and writeable by www-data

More info: https://library.linode.com/web-servers/nginx/python-uwsgi/ubuntu-12.04-precise-pangolin
Database schema
================
CREATE TABLE device_status(id integer primary key, device_id integer, status integer, last_update integer);

CREATE TABLE devices(device_id integer, name text, type integer);

CREATE TABLE events(id integer primary key, device_id integer, auto integer, type integer, fire_at integer);

CREATE TABLE sensor_data(id integer primary key, device_id integer, value text, timestamp integer, type integer);


Upcoming features
=================
* Show temperature graphs for logged temperature data
