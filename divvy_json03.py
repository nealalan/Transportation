import urllib.request
import requests
import json

##grab the live json dataset
url = 'https://www.divvybikes.com/stations/json'
req = urllib.request.Request(url)

##parse response into object
r = urllib.request.urlopen(req).read()
divvy = json.loads(r.decode('utf-8'))

homeStation = 100
counter = 0
availableBikes = 0
availableDocks = 0
noBikes = 0
noDocks = 0
badCnt = 0
badTot = 0
systemWideDocks = 0

print("DIVVY BIKE DATA REPORTING")

#rows = []
#rows.append({"ID":"1", "name":"Cat", "year":"1998", "priority":"1"})

for item in divvy['stationBeanList']:
    counter += 1
    availableBikes += item['availableBikes']
    availableDocks += item['availableDocks']
    systemWideDocks += item['totalDocks']
    # print station with no avail bikes
    if item['availableBikes'] == 0:
        noBikes += 1
        if noBikes == 1:
            print("Stations with no available bikes:")
        print('{:{width}}'.format(item['stationName'], width=36),
            " Bikes:", '{0:{width}}'.format(item['availableBikes'], width=2),
            " Docks:", '{0:{width}}'.format(item['availableDocks'], width=2),
            " TotalDocks:", '{0:{width}}'.format(item['totalDocks'], width=3))

for item in divvy['stationBeanList']:
    if item['availableDocks'] == 0:
        noDocks += 1
        if noDocks == 1:
            print("\nStations with no available docks:")
        print('{:{width}}'.format(item['stationName'], width=36),
            " Bikes:", '{0:{width}}'.format(item['availableBikes'], width=2),
            " Docks:", '{0:{width}}'.format(item['availableDocks'], width=2),
            " TotalDocks:", '{0:{width}}'.format(item['totalDocks'], width=3))

for item in divvy['stationBeanList']:
    if item['availableBikes'] + item['availableDocks'] != item['totalDocks']:
        badCnt += 1
        if badCnt == 1:
                print("\nStation with bad bike or dock (3+):")
        badStation = item['availableBikes'] + item['availableDocks'] - item['totalDocks']
        badTot = badTot + badStation
        if abs(badStation) > 2:
            print('{:{width}}'.format(item['stationName'], width=36),
                " Bikes:", '{0:{width}}'.format(item['availableBikes'], width=2),
                " Docks:", '{0:{width}}'.format(item['availableDocks'], width=2),
                " TotalDocks:", '{0:{width}}'.format(item['totalDocks'], width=3),
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

for item in divvy['stationBeanList']:
    if item['id'] == homeStation:
        print('\nHOME STATION STATUS:', item['stationName'])
        print("Bikes:", item['availableBikes'], " Docks:", item['availableDocks'], " TotalDocks:", item['totalDocks'])
