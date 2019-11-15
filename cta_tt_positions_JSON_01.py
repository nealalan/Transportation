################################################################################
## Neal Dreher 20171209 nealalan.com
## Python3 Script
##
## PROJECT:
##  CHICAGO TRANSIT AUTHORITY "CTA" TRAIN TRACKER API
##      http://www.transitchicago.com/developers/traintracker.aspx
##      http://www.transitchicago.com/developers/ttdocs/default.aspx
##
## INPUT:
##  READ IN CTA TRAIN POSITION DATA AND PARSE IT OUT
##  ADD TO URL FOR JSON: &outputType=JSON
##
## OUTPUT:
##
##
################################################################################
#
# INPUT DATA FORMAT
#{'ctatt':
# {'tmst': '2018-03-05T01:59:10',
# 'errCd': '0',
# 'errNm': None,
# 'route': [{'@name': 'g'},
#           {'@name': 'y',
#            'train': {'rn': '030',
#                      .....
#                      'heading': '302'}
#           {'@name': 'blue',
#            'train': [{'rn': '125',
#                        'destSt': '30171',
#                        'destNm': "O'Hare",
#                          'trDr': '1',
#                     'nextStaId': '40320',
#                     'nextStpId': '30062',
#                     'nextStaNm': 'Division',
#                          'prdt': '2018-03-05T01:58:40',
#                          'arrT': '2018-03-05T02:00:40',
#                         'isApp': '0',
#                         'isDly': '0',
#                         'flags': None,
#                           'lat': '41.89932', 'lon': '-87.66022',
#                       'heading': '302'},
#                      {'rn': '127', 'destSt': '30171', 'destNm': "O'Hare", 'trDr': '1', 'nextStaId': '40750', 'nextStpId': '30145', 'nextStaNm': "Harlem (O'Hare Branch)", 'prdt': '2018-03-05T01:58:33', 'arrT': '2018-03-05T02:00:33', 'isApp': '0', 'isDly': '0', 'flags': None, 'lat': '41.98244', 'lon': '-87.7851', 'heading': '278'},
################################################################################
################################################################################
import sys, time
import datetime
import requests
import json
import urllib.request
#from bs4 import BeautifulSoup
import secretapikey

DATETIME_JSON_FORMAT = '%Y-%m-%dT%H:%M:%S'

## GET THE DIFFERENCE IN MINUTES BETWEEN TWO DATE TIMES
def text_time_difference_minutes(dt1):
    dt1 = datetime.datetime.strptime(dt1 , DATETIME_JSON_FORMAT)
    return round(abs(dt1-(datetime.datetime.now())).total_seconds() / 60)

## SET THE NAME OF THE LINE TO SOMETHING MORE USER FRIENDLY
def expand_lines_name(arg):
    switcher = {
        "g": "Green ",
        "brn": "Brown ",
        "org": "Orange",
        "blue": "Blue  ",
        "red": "Red   ",
        "pink": "Pink  ",
        "p": "Purple",
        "y": "Yellow"
    }
    return switcher.get(arg)

def train_run_print_line(line_name, arg):
    nextStation = arg['nextStaNm']
    run = arg['rn']
    stopID = arg['nextStpId']
    trainDestination = arg['destNm']
    estArrivalTime = arg['arrT']
    print('{00:{width}}'.format(text_time_difference_minutes(estArrivalTime),width=2), "min", expand_lines_name(line_name), "run", run, "to",'{:{width}}'.format(trainDestination,width=14), trainDestination, stopID, "is next.")
    return


## ACCESS THE CTA DATASET - TRAIN ARRIVALS BY A PARTICULAR STATION
map_id = "40380"
route_id = "G,Blue,Red,Brn,Y,Org,Pink,P"
file_format = "&outputType=JSON"
url = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key=" + secretapikey.cta_api_key + "&rt=" + route_id + file_format
## need error handling code for when the site can't be reached or internet connectivity is down
req = urllib.request.Request(url)
print(url)

##PARSE RESPONSE INTO A DICTIONARY OBJECT
r = urllib.request.urlopen(req).read() # bytes of data
trains_data = json.loads(r.decode('utf-8')) # dict object

## PRINT THE ENTIRE DATASET RECEIVED
#print(trains_data)

## CHECK FOR REQUEST ERRORS
if (trains_data['ctatt']['errCd'] != '0'): print("ERROR: ", trains_data['ctatt']['errCd'])

## CHECK THE TIMESTAMP OF THE DATA VS THE CURRENT TIME
if text_time_difference_minutes(trains_data['ctatt']['tmst']) != 0:
    print("DATA DELAY: ", text_time_difference_minutes(trains_data['ctatt']['tmst']), "minutes")

## REPORT HEADING
print("\nCTA TRAIN POSITIONS", datetime.datetime.strptime(trains_data['ctatt']['tmst'], '%Y-%m-%dT%H:%M:%S'), "\n")

## PARSE DATASET
# trains_data file / ctatt dataset / route by color / train run
# - loop through the routes to pull out the color
# - validate the route has runs using .get
# - loop through the runs within the routes
# - extract the data for the train
count = 0
for train_rt in trains_data['ctatt']['route']:
    line_name = train_rt['@name']
    if train_rt.get('train') != None:
        for train_run in train_rt['train']:
            train_run_print_line(line_name, train_run)
            count = count + 1

quit()


######
#for train_rt in trains_data['ctatt']['route']:
#    line_name = train_rt['@name']
#
#    train_runs = train_rt.get('train', [])
#    if not isinstance(train_runs, list):
#        # single entry, wrap
#        train_runs = [train_runs]
#
#    for train_run in train_runs:
#        # ...
