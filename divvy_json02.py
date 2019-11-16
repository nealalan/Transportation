###############################################################################
# neal dreher 2017-12-09, updated 2019-11-15
# https://github.com/nealalan/Transportation/blob/master/divvy_json02.py
#
# INFO: This python3 script will pull publically available JSON datasets containing
#       realtime data for the Chicago DIVVY Bike Share Stations
#
# dependencies:
# $ pip3 install requests thespian
# use:
# $ python3 divvy_json02.py 
# 
# DIVVY UPDATED THEIR DATASETS (between 2018 and 2019)
# - station names are no longer available in a single dataset => add code 
#   to read the stationName from the stationID
# - the method of reporting TOTAL DOCKS vs AVAIL DOCKS no longer works
#   the same => pull from CAPACITY in StationInfo file
#
###############################################################################
# JSON DATA LAYOUT
#
# Station Status (realtime counts) -- 'https://gbfs.divvybikes.com/gbfs/en/station_status.json'
#
# {"last_updated":1573850008,"ttl":2,"data":
#  {"stations":
#   {"station_id":"331","num_bikes_available":7,"num_ebikes_available":0,"num_bikes_disabled":0,
#    "num_docks_available":20,"num_docks_disabled":0,"is_installed":1,
#    "is_renting":1,"is_returning":1,"last_reported":1573849499,"eightd_has_available_keys":false},
# ]}}
#
# System information (station information) -- 'https://gbfs.divvybikes.com/gbfs/en/station_information.json'
#
# {"last_updated":1573852861,"ttl":2,"data":
#  {"stations":[
#   {"station_id":"331","external_id":"a3aacf29-a135-11e9-9cda-0a87ae2ba916",
#    "name":"Halsted St & Clybourn Ave",
#    "short_name":"331","lat":41.909668,"lon":-87.648128,"rental_methods":["CREDITCARD","TRANSITCARD","KEY"],
#    "capacity":27,"electric_bike_surcharge_waiver":false,"eightd_has_key_dispenser":false,"has_kiosk":true}
# ]}}
#
###############################################################################
## Total docks = bike available + bikes unavailable + docks avail + docks unavail
##   this is also the "capacity" field in Station Information dataset
#
# Note: There is no way to account for valet stations with bikes locked by cable vs to a dock
###############################################################################

import urllib.request
import requests
import json

## LITERALS
homeStation = ['331', '333']  # Halsted & Clybourn
DATASETNAME = 'stations' # was 'stationBeanList'
AVAILBIKES = 'num_bikes_available'
AVAILDOCKS = 'num_docks_available'
UNAVAILBIKES = 'num_bikes_disabled'
UNAVAILDOCKS = 'num_docks_disabled'
STATIONID = 'station_id'
STATIONNAME = 'name'
TOTALDOCKS = 'capacity'

## VARS
counter = 0
availableBikes = 0
availableDocks = 0
noBikes = 0
noDocks = 0
badCnt = 0
badTot = 0
systemWideDocks = 0

## GRAB THE LIVE JSON DATASET FROM DIVVY
#OLD url = 'https://www.divvybikes.com/stations/json'
## request data and parse into object
stationStatusURL = 'https://gbfs.divvybikes.com/gbfs/en/station_status.json'
divvyStationStatusReponse = urllib.request.urlopen(urllib.request.Request(stationStatusURL)).read()
divvyStationStatusDataset = json.loads(divvyStationStatusReponse.decode('utf-8'))
stationInfoURL = 'https://gbfs.divvybikes.com/gbfs/en/station_information.json'
divvyStationInfoResponse = urllib.request.urlopen(urllib.request.Request(stationInfoURL)).read()
divvyStationInfoDataSet = json.loads(divvyStationInfoResponse.decode('utf-8'))

## accums for the DATA SUMMARY section
def counters(passed_item, passed_station):
    global counter, availableBikes, availableDocks, systemWideDocks
    counter += 1
    availableBikes += passed_item[AVAILBIKES]
    availableDocks += passed_item[AVAILDOCKS]
    systemWideDocks += passed_item[AVAILBIKES] + passed_item[AVAILDOCKS] + passed_item[UNAVAILBIKES] + passed_item[UNAVAILDOCKS]

    global badCnt, badTot, noDocks, noBikes
    # count empty or full stations
    if passed_item[AVAILDOCKS] == 0:
        noDocks += 1
    if passed_item[AVAILBIKES] == 0:
        noBikes += 1
    # account for bad station and equip totals
    badTot += badStation
    if badStation > 0:
        badCnt = badCnt + 1
        #print('Sta:', badStation, ' Tot:', badTot, ' Cnt:', badCnt)

## format each output line item, 
##  including a read of the text name from a different dataset
def printers(passed_item, passed_station):

    # print the line
    print('{:{width}}'.format(passed_item[STATIONID], width=3),
        '{:36.36}'.format(passed_station[STATIONNAME]),
        " Bikes:", '{0:{width}}'.format(passed_item[AVAILBIKES], width=2),
        " Docks:", '{0:{width}}'.format(passed_item[AVAILDOCKS], width=2),
        " TotalDocks:", '{0:{width}}'.format(
            passed_station[TOTALDOCKS], width=3),
            #passed_item[AVAILBIKES] + passed_item[AVAILDOCKS] + 
            #passed_item[UNAVAILBIKES] + passed_item[UNAVAILDOCKS], width=3),
        " Errors:", '{0:{width}}'.format(abs(badStation), width=2))

## RUN SCRIPT STARTING HERE
print("DIVVY BIKE DATA REPORTING")

## LIST ALL STATIONS, SHOW WITH ERRORS
for item in divvyStationStatusDataset['data'][DATASETNAME]:
    for station in divvyStationInfoDataSet['data'][DATASETNAME]:
        if station[STATIONID] == item[STATIONID]:
            badStation = station[TOTALDOCKS] - (item[AVAILBIKES] + item[AVAILDOCKS])
            counters(item, station)
            printers(item, station)

## PRINT SUMMARY
print("\nDIVVY BIKE DATA SUMMARY\n",
      "     Total Stations:", '{0:{width}}'.format(counter, width=5),
      "             Stations with no bikes:", '{0:{width}}'.format(noBikes, width=4), "\n",
      "        Total Docks:", '{0:{width}}'.format(systemWideDocks, width=5),
      "             Stations with no docks:", '{0:{width}}'.format(noDocks, width=4), "\n",
      "        Avail Bikes:", '{0:{width}}'.format(availableBikes, width=5),
      "      Stations w/ potential repairs:", '{0:{width}}'.format(badCnt, width=4), "\n",
      "        Avail Docks:", '{0:{width}}'.format(availableDocks, width=5),
      "     Equipment w/ potential repairs:", '{0:{width}}'.format(abs(badTot), width=4))
