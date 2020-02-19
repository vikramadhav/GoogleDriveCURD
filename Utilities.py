import os
import json
import argparse

def file_size(fname):
    statinfo = os.stat(fname)
    return statinfo.st_size

# Open the JSOn configuration file and Fetch Data
with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
    data = json.load(config_file)



# Get Command line arguments
def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rt', '--runType',
                    help='Pass Run Type , 1 for Upload versu other options to download and delete',
                    action="store", required=False)
    return parser.parse_args()