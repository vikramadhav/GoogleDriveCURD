import os
import json
import argparse
import pybreaker

# Provide the File Size
def file_size(fname):
    statinfo = os.stat(fname)
    return statinfo.st_size

configdata = None
db_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

# Open the JSOn configuration file and Fetch Data
def readJsonData():
    with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
        return json.loads(config_file.read())


def updateJsonData(data):
    with open(os.path.join(os.getcwd(), 'config.json'), 'w') as config_file:
        json.dump(data, config_file)


# Get Command line arguments
def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rt', '--runType',
                        help='Pass Run Type , 1 for Upload versu other options to download and delete',
                        action="store", required=False)
    return parser.parse_args()

if not configdata:
    configdata = readJsonData()