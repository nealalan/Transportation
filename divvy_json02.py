import urllib.request
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
for item in divvy['stationBeanList']:
    counter += 1
    availableBikes += item['availableBikes']
    availableDocks += item['availableDocks']
    systemWideDocks += item['totalDocks']
    if item['availableBikes'] == 0:
        noBikes += 1
        if noBikes == 1:
            print("Stations with no available bikes:")
        print(item['stationName'], " Bikes:", item['availableBikes'], " Docks:", item['availableDocks'], " TotalDocks:", item['totalDocks'])

for item in divvy['stationBeanList']:
    if item['availableDocks'] == 0:
        noDocks += 1
        if noDocks == 1:
            print("\nStations with no available docks:")
        print(item['stationName'], " Bikes:", item['availableBikes'], " Docks:", item['availableDocks'], " TotalDocks:", item['totalDocks'])

for item in divvy['stationBeanList']:
    if item['availableBikes'] + item['availableDocks'] != item['totalDocks']:
        badCnt += 1
        if badCnt == 1:
                print("\nStation with bad bike or dock (3+):")
        badStation = item['availableBikes'] + item['availableDocks'] - item['totalDocks']
        badTot = badTot + badStation
        if abs(badStation) > 2:
            print(item['stationName'], " Bikes:", item['availableBikes'], " Docks:", item['availableDocks'], " TotalDocks:", item['totalDocks'], " Errors:", abs(badStation))

print("\nDIVVY BIKE DATA SUMMARY")
print("Total Stations:", counter, " Total Docks:", systemWideDocks)
print("Avail Bikes:", availableBikes, " Avail Docks:", availableDocks)
print("Stations with no bikes:", noBikes, " Stations with no docks:", noDocks)
print("Stations w/ potential repairs:", badCnt, " Equipment w/ potential repairs:", abs(badTot))

for item in divvy['stationBeanList']:
    if item['id'] == homeStation:
        print('\nHOME STATION STATUS:', item['stationName'])
        print("Bikes:", item['availableBikes'], " Docks:", item['availableDocks'], " TotalDocks:", item['totalDocks'])
