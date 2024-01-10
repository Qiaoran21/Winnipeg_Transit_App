"""
Description: Winnipeg Transit App
Author: Qiaoran 
Date Created: 2024-01-03

Updates: 2024-01-04
"""

import json
from requests import get
from dateutil.parser import parse


#List all the bus stops with in a certain distance of a set of gps coordinates.
API_KEY = "3o2msv0zVbCVgvt-XRgB"
lon = -97.131
lat = 49.891
distance = 500 

url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"


response = get(url_stops)
resp_stops = response.json()

stops = resp_stops.get('stops')

print("Stops available " + str(distance)
      + "m from coordinates (" + str(lat) + ", " + str(lon) + "):")

#Get stop numbers and names for the stops within range.
for stop in stops:
    stop_number = stop.get('number')
    stop_name = stop.get('name')

    print('\t', str(stop_number), str(stop_name))

#Get user to enter a bus stop number from the list above. 
user_input = input("Enter stop number:")

#List all the scheduled and estimated arrival times of the chosen bus stop. 
print("Arrival times: " )

url_schedules = f"https://api.winnipegtransit.com/v3/stops/{user_input}/schedule.json?api-key={API_KEY}"

response = get(url_schedules)
resp_schedules = response.json()

schedules = resp_schedules.get('stop-schedule').get('route-schedules')

if schedules:

    for schedule in schedules:
        for scheduled_stop in schedule.get('scheduled-stops'):
            times = scheduled_stop.get('times')

            if times:
                arrival = times.get('arrival')

                if arrival:
                    scheduled = parse(arrival.get('scheduled'))
                    estimated = parse(arrival.get('estimated'))

                    print('\t', "Scheduled: " + str(scheduled.strftime("%H:%M:%S")),
                          '\t', "Estimated: " + str(estimated.strftime("%H:%M:%S")))

else:
    print("No schedules available!")

