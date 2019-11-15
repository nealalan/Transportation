## Neal Dreher 20171209 nealalan.com
## Python3 Script
##
## CHICAGO TRANSIT AUTHORITY "CTA" TRAIN TRACKER API
## http://www.transitchicago.com/developers/traintracker.aspx
## http://www.transitchicago.com/developers/ttdocs/default.aspx
##
## READ IN CTA TRAIN ARRIVAL DATA AND PARSE IT OUT
##
## ADD TO URL FOR JSON: &outputType=JSON
##
## ctatt           Root element
## ./tmst          Shows time when response was generated in format: yyyyMMdd HH:mm:ss (24-hour format, time local to Chicago)
## ./errCd         Numeric error code (see appendices)
## ./errNm         Textual error description/message (see appendices)
## ./route name=   Container element (one per route in response), name attribute indicates route per GTFS-matching route identifiers (see appendices)
## ././train       Container element (one per train in response)
## ./././rn        Run number
## ./././destSt    GTFS unique stop ID where this train is expected to ultimately end its service run (experimental and supplemental only—see note below)
## ./././destNm    Friendly destination description (see note below)
## ./././trDr      Numeric train route direction code (see appendices)
## ./././nextStaId Next station ID (parent station ID matching GTFS)
## ./././nextStpId Next stop ID (stop ID matching GTFS)
## ./././nextStaNm Proper name of next station
## ./././prdt      Date-time format stamp for when the prediction was generated: yyyyMMdd HH:mm:ss (24-hour format, time local to Chicago)
## ./././arrT      Date-time format stamp for when a train is expected to arrive/depart: yyyyMMdd HH:mm:ss (24-hour format, time local to Chicago)
## ./././isApp     Indicates that Train Tracker is now declaring “Approaching” or “Due” on site for this train
## ./././isDly     Boolean flag to indicate whether a train is considered “delayed” in Train Tracker
## ./././flags     Train flags (not presently in use)
## ./././lat       Latitude position of the train in decimal degrees
## ./././lon       Longitude position of the train in decimal degrees
## ./././heading   Heading, expressed in standard bearing degrees (0 = North, 90 = East, 180 = South, and 270 = West; range is 0 to 359, progressing clockwise)
##

import sys, time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import secretapikey

## GET THE DIFFERENCE IN MINUTES BETWEEN TWO DATE TIMES
def text_time_difference_minutes(dt1):
    dt1 = datetime.strptime(dt1 , '%Y%m%d %H:%M:%S')
    return round(abs(dt1-(datetime.now())).total_seconds() / 60)

## SET THE NAME OF THE LINE TO SOMETHING MORE USER FRIENDLY
def expand_lines_name(arg):
    switcher = {
        "G": "Green ",
        "Brn": "Brown ",
        "Org": "Orange",
        "Blue": "Blue  ",
        "Red": "Red   ",
        "Pink": "Pink  "
    }
    return switcher.get(arg, route[count].get_text())

## ACCESS THE CTA DATASET - TRAIN ARRIVALS BY A PARTICULAR STATION
map_id = "40380"
url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=" + secretapikey.cta_api_key + "&mapid=" + map_id
req = requests.get(url)

## CHECK FOR HTTP REQUEST ERRORS, 200 = OK
if (req.status_code != 200): print("ERROR: ", req.status_code)
if (req.status_code >= 400 | req.status_code <= 499): print("You messed up!")
if (req.status_code >= 500 | req.status_code <= 599): print("Server messed up!")

## PRINT THE ENTIRE DATASET RECEIVED
#print(req.text)

##PARSE RESPONSE USING BeautifulSoup4
train_arrivals = BeautifulSoup(req.text, 'xml')
#print(type(train_arrivals))
errCd = train_arrivals.find_all('errCd')
if (errCd[0].get_text() != "0"): print("Source data error: ", errCd)
tmst = train_arrivals.find_all('tmst')

##PARSE DATA FROM RESPONSE
stations = train_arrivals.find_all('staNm')
run = train_arrivals.find_all('rn')
route = train_arrivals.find_all('rt')
stopDestinations = train_arrivals.find_all('stpDe')
trainDestination = train_arrivals.find_all('destNm')
estArrivalTime = train_arrivals.find_all('arrT')

print(text_time_difference_minutes(tmst[0].get_text()))

print("\nCTA DATA", tmst[0].get_text(), "FOR", stations[0].get_text(), "\n")

count = 0
for item in stations:
    print(
        '{00:{width}}'.format(text_time_difference_minutes(estArrivalTime[count].get_text()),width=2),
        "min ", expand_lines_name(route[count].get_text()),
        run[count].get_text(),
        "to",'{:{width}}'.format(trainDestination[count].get_text(),width=14),
        stopDestinations[count].get_text())
    count = count + 1
