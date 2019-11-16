################################################################################
# Neal Dreher 20171209  updated 2019-11-15
# https://github.com/nealalan/Transportation/blob/master/cta_tt_positions_JSON_01.py
#
# PROJECT:
#  CHICAGO TRANSIT AUTHORITY "CTA" TRAIN TRACKER API
#      http://www.transitchicago.com/developers/traintracker.aspx
#      http://www.transitchicago.com/developers/ttdocs/default.aspx
#
# INPUT:
#  READ IN CTA TRAIN POSITION DATA AND PARSE IT OUT
#  ADD TO URL FOR JSON: &outputType=JSON
#
# OUTPUT:
# CTA TRAIN POSITIONS 2019-11-15 18:47:43

#  2 min Green  run 013 to Harlem/Lake    Harlem/Lake 30033 is next.
#  3 min Green  run 014 to Harlem/Lake    Harlem/Lake 30099 is next.
#  1 min Green  run 017 to Ashland/63rd   Ashland/63rd 30032 is next.
################################################################################
# JSON DATA LAYOUT
#
#{'ctatt':
# {'tmst': '2018-03-05T01:59:10','errCd': '0','errNm': None,
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
# ]}]}}
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

def train_run_print_line(line_name, runItem):
    run = runItem['rn']
    stopID = runItem['nextStpId']
    stopName = runItem['nextStaNm']
    trainDestination = runItem['destNm']
    estArrivalTime = runItem['arrT']
    print('{00:{width}}'.format(text_time_difference_minutes(estArrivalTime),width=2), 
        "min", expand_lines_name(line_name), 
        "run", run, 
        "to",'{:{width}}'.format(trainDestination,width=14),
        stopName, "is next.")


## ACCESS THE CTA DATASET 
#  - TRAIN ARRIVALS BY A PARTICULAR STATION
# need error handling code for when the site can't be reached or internet connectivity is down
base_url = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key="
map_id = "40380"
route_id = "&rt=G,Blue,Red,Brn,Y,Org,Pink,P"
file_format = "&outputType=JSON"
trainTrackerPositionsURL = urllib.request.Request(base_url + secretapikey.cta_api_key + route_id + file_format)
trainTrackerPositionsResponse = urllib.request.urlopen(trainTrackerPositionsURL).read() # bytes of data
trainTrackerPositionsDataset = json.loads(trainTrackerPositionsResponse.decode('utf-8')) # dict object

## CHECK FOR REQUEST ERRORS
if (trainTrackerPositionsDataset['ctatt']['errCd'] != '0'): 
    print("ERROR: ", trainTrackerPositionsDataset['ctatt']['errCd'])

## CHECK THE TIMESTAMP OF THE DATA VS THE CURRENT TIME
# Print a data delay if the time stamp is not current
if text_time_difference_minutes(trainTrackerPositionsDataset['ctatt']['tmst']) != 0:
    print("DATA DELAY: ", text_time_difference_minutes(trainTrackerPositionsDataset['ctatt']['tmst']), "minutes")

## REPORT HEADING
print("\nCTA TRAIN POSITIONS", datetime.datetime.strptime(trainTrackerPositionsDataset['ctatt']['tmst'], '%Y-%m-%dT%H:%M:%S'), "\n")

## PARSE DATASET
# trainTrackerPositionsDataset file / ctatt dataset / route by color / train run
# - loop through the ROUTE to pull out the color
# - validate the route has runs in an array
#    Issue with parsing train lines that are single or empty! Need to handle no 'train' key: 
#      {"@name":"y"},{"@name":"org","train":[{"rn":
#      {"@name":"p","train":{"rn":"517",
#      {"@name":"g","train":[{"rn":"015",
#   https://stackoverflow.com/questions/49183806/coding-python-to-handle-json-array-inconsistencies
# - loop through the runs within the routes
# - extract the data for the train

count = 0
# for route in trainTrackerPositionsDataset['ctatt']['route']:
#     line = route['@name']
#     if route['train']:
#         for run in route['train']:
#             train_run_print_line(line, run)
#             count = count + 1

for train_rt in trainTrackerPositionsDataset['ctatt']['route']:
    line_name = train_rt['@name']
    # if no runs, return empty data
    train_runs = train_rt.get('train', [])
    if not isinstance(train_runs, list):
        # single entry, wrap
        train_runs = [train_runs]
    for train_run in train_runs:
        train_run_print_line(line_name, train_run)
        count = count + 1

print('Currently', count, 'runs.')
