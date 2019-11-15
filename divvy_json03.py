###############################################################################
## neal dreher 2017-12-09
##   updated 2019-11-15
##
## dependencies:
## $ pip3 install requests thespian
##
## use:
## $ python3 divvy_json03.py 
## 
## DIVVY UPDATED THEIR DATASETS
## - station names are no longer in the available dataset, need to add code 
##   to read the stationName from the stationID
## - the method of reporting TOTAL DOCKS vs AVAIL DOCKS no longer works the same,
##   so a different method of analyzing stations with errors needs determined
#
# Station Status (realtime counts) -- 'https://gbfs.divvybikes.com/gbfs/en/station_status.json'
# {"last_updated":1573850008,"ttl":2,"data":{"stations":
#   {"station_id":"331","num_bikes_available":7,"num_ebikes_available":0,"num_bikes_disabled":0,
#    "num_docks_available":20,"num_docks_disabled":0,"is_installed":1,
#    "is_renting":1,"is_returning":1,"last_reported":1573849499,"eightd_has_available_keys":false},
# ]}}
#
# System information (station information) -- 'https://gbfs.divvybikes.com/gbfs/en/station_information.json'
# {"last_updated":1573852861,"ttl":2,"data":{"stations":[
#   {"station_id":"331","external_id":"a3aacf29-a135-11e9-9cda-0a87ae2ba916",
#    "name":"Halsted St & Clybourn Ave",
#    "short_name":"331","lat":41.909668,"lon":-87.648128,"rental_methods":["CREDITCARD","TRANSITCARD","KEY"],
#    "capacity":27,"electric_bike_surcharge_waiver":false,"eightd_has_key_dispenser":false,"has_kiosk":true}
# ]}}
###############################################################################

import urllib.request
import requests
import json

##grab the live json dataset
#url = 'https://www.divvybikes.com/stations/json'
url = 'https://gbfs.divvybikes.com/gbfs/en/station_status.json'
# stationInfoURL = 'https://gbfs.divvybikes.com/gbfs/en/station_information.json'
req = urllib.request.Request(url)

##parse response into object
r = urllib.request.urlopen(req).read()
divvy = json.loads(r.decode('utf-8'))

homeStation = 331  # Halsted & Clybourn
counter = 0
availableBikes = 0
availableDocks = 0
noBikes = 0
noDocks = 0
badCnt = 0
badTot = 0
systemWideDocks = 0

## LITERALS
DATASETNAME = 'stations' # was 'stationBeanList'
AVAILBIKES = 'num_bikes_available'
AVAILDOCKS = 'num_docks_available'
UNAVAILBIKES = 'num_bikes_disabled'
UNAVAILDOCKS = 'num_docks_disabled'
STATIONID = 'station_id'
print("DIVVY BIKE DATA REPORTING")

#rows = []
#rows.append({"ID":"1", "name":"Cat", "year":"1998", "priority":"1"})

for item in divvy['data'][DATASETNAME]: 
    counter += 1
    availableBikes += item[AVAILBIKES]
    availableDocks += item[AVAILDOCKS]
    systemWideDocks += item[AVAILDOCKS] + item[UNAVAILBIKES]
    # print station with no avail bikes
    if item[AVAILBIKES] == 0:
        noBikes += 1
        if noBikes == 1:
            print("Stations with no available bikes:")
        print('{:{width}}'.format(item[STATIONID], width=36),
            " Bikes:", '{0:{width}}'.format(item[AVAILBIKES], width=2),
            " Docks:", '{0:{width}}'.format(item[AVAILDOCKS], width=2),
            " TotalDocks:", '{0:{width}}'.format(item[AVAILDOCKS] + item[UNAVAILBIKES], width=3))

for item in divvy['data'][DATASETNAME]:
    if item[AVAILDOCKS] == 0:
        noDocks += 1
        if noDocks == 1:
            print("\nStations with no available docks:")
        print('{:{width}}'.format(item[STATIONID], width=36),
            " Bikes:", '{0:{width}}'.format(item[AVAILBIKES], width=2),
            " Docks:", '{0:{width}}'.format(item[AVAILDOCKS], width=2),
            " TotalDocks:", '{0:{width}}'.format(item[AVAILDOCKS] + item[UNAVAILBIKES], width=3))

for item in divvy['data'][DATASETNAME]:
    if item[UNAVAILBIKES] > 1 | item[UNAVAILDOCKS] > 1:
        badCnt += 1
        if badCnt == 1:
                print("\nStation with bad bike or dock (3+):")
        badStation = item[AVAILBIKES] + item[AVAILDOCKS] - (item[AVAILDOCKS] + item[UNAVAILBIKES])
        badTot = badTot + badStation
        if abs(badStation) > 2:
            print('{:{width}}'.format(item[STATIONID], width=36),
                " Bikes:", '{0:{width}}'.format(item[AVAILBIKES], width=2),
                " Docks:", '{0:{width}}'.format(item[AVAILDOCKS], width=2),
                " TotalDocks:", '{0:{width}}'.format(item[AVAILDOCKS] + item[UNAVAILBIKES], width=3),
                " Errors:", '{0:{width}}'.format(abs(badStation), width=2))

print("\nDIVVY BIKE DATA SUMMARY\n",
      "     Total Stations:", '{0:{width}}'.format(counter, width=5),
      "             Stations with no bikes:", '{0:{width}}'.format(noBikes, width=4), "\n",
      "        Total Docks:", '{0:{width}}'.format(systemWideDocks, width=5),
      "             Stations with no docks:", '{0:{width}}'.format(noDocks, width=4), "\n",
      "        Avail Bikes:", '{0:{width}}'.format(availableBikes, width=5),
      "      Stations w/ potential repairs:", '{0:{width}}'.format(badCnt, width=4), "\n",
      "        Avail Docks:", '{0:{width}}'.format(availableDocks, width=5),
      "     Equipment w/ potential repairs:", '{0:{width}}'.format(abs(badTot), width=4))

for item in divvy['data'][DATASETNAME]:
    if item[STATIONID] == homeStation:
        print('\nHOME STATION STATUS:', item[STATIONID])
        print("Bikes:", item[AVAILBIKES], " Docks:", item[AVAILDOCKS], " TotalDocks:", item[AVAILDOCKS] + item[UNAVAILBIKES])
