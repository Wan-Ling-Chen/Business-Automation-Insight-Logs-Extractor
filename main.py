import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

for package in ['requests', 'pyyaml']:
  import_or_install(package)

import json
import csv
import requests.packages.urllib3
import yaml
from yaml.loader import SafeLoader
import argparse
import re


requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="config file name")
args = parser.parse_args()
config_filename = args.config

if config_filename is None:
    # Default config filename
    config_filename = "config.yaml"

# Load the config
try:
    with open(config_filename, 'r') as config_file:
        config = yaml.load(config_file, Loader=SafeLoader)
except FileNotFoundError as e:
    msg = "Cannot find config file : config.yaml or the config file specified in arguments"
    print(msg)

# Apply config to global variables
ROOT_URL = config['host']
USER = config['user']
PWD = config['password']
INDEX = config['index-name']
START_TIME  = config['start-time']
END_TIME = config['end-time']
SEARCH_TIME_COLUMN = config['search-time-column']
COLUMN_MAPPING = config['csv-column-mapping']
BUSINESS_DATA = config['business-data']
is_export_es_rawdata = config['is_export_es_rawdata']

if START_TIME:
  START_TIME  = START_TIME.strftime("%Y-%m-%dT%H:%M:%SZ")
if END_TIME:
  END_TIME  = END_TIME.strftime("%Y-%m-%dT%H:%M:%SZ")
if not COLUMN_MAPPING:
  COLUMN_MAPPING = {'processId':'processInstanceId', 'activityId':'name','startTime':'startTime', 'endTime':'completedTime', 'role':'performerName'}

if not INDEX:
  response = requests.get(f'{ROOT_URL}/_mapping', verify=False, auth=(USER, PWD))
  all_indices = json.loads(response.content)
  all_indices = all_indices.keys()
  for index in all_indices:
    if re.search("^icp4ba-bai-process-summaries-completed-idx-ibm-bai-", index):
      INDEX = index

data = {
    "query": {
        "range": {  # expect this to return the one result on 2012-12-20
            SEARCH_TIME_COLUMN: {
                "gte":START_TIME, 
                "lte":END_TIME,
            }
        }
    }
}
response = requests.get(f'{ROOT_URL}/{INDEX}/_search?pretty', json=data, verify=False, auth=(USER, PWD))

if is_export_es_rawdata == 'Y':
  with open('es_rawdata.text', 'w', newline='') as f:
      f.write(response.text)

with open('output.csv', 'w', newline='') as csvfile:
  # 定義欄位
  fieldnames = COLUMN_MAPPING.keys()
  if BUSINESS_DATA:
    fieldnames = list(fieldnames) + list(BUSINESS_DATA.keys())
  # 將 dictionary 寫入 CSV 檔
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  # 寫入第一列的欄位名稱
  writer.writeheader()

  # 寫入資料
  context = json.loads(response.text)['hits']['hits']
  for c in context:
    line = c['_source']
    data_dict = {}
    for key, value in COLUMN_MAPPING.items():
        data_dict[key] = line.get(value, None)
    for key, value in BUSINESS_DATA.items():
      data_dict[key] = list(line['data'].values())[0].get(value, None)
    writer.writerow(data_dict)

