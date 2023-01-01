
# Business Automation Insight (BAI) Extraction Utility ＆ ProcessMining Demo
A simple utility to extract Business Automation Insight (BAI) instance data (from Elasticsearch) and export it as a CSV.


# Background Intro
If we already have Business Automation Workflow (BAW), a BPMS, we want to do health checks of processes. This BAI Extraction Utility helps extract valuable data and transform logs into the correct format for further usage of Process Mining.

When we use BAW, Business Automation Insight(BAI) acts as its monitor and real-time dashboard.
The mechanism behind BAI is that every transaction or operation generated in BAW will be recorded as event logs and automatically collected in Elasticsearch.

What is Process Mining? <br />
A tool applies data science to discover, validate and improve workflows. 
In other words, Process Mining can visualize the current status of processes and identify bottlenecks.
The below demo video introduces more details of Process Mining.

## Pre-Requirement
Just a recent version of python3. <br />
https://www.python.org/downloads/

The easiest way is to download and unpack the zip file.

## Config
config file: `config.yaml` <br />
Optional parameters have default values based on below example or remain empty.

IPM example:
https://community.ibm.com/community/user/automation/blogs/michele-chilanti1/2021/08/31/process-mining-primer

Default Value: <br />
**index-name** : 'icp4ba-bai-process-summaries-completed-idx-ibm-bai-xxxxxxxxx' <br />
**csv-column-mapping** : {'processId':'processInstanceId', 'activityId':'name','startTime':'startTime', 'endTime':'completedTime', 'role':'performerName'}

p.s. key is csv export column name, value is Elasticsearch field name

## Execute
python3 main.py

## Process Mining Demo Link

Short Version (Chinese Version):
https://media.github.ibm.com/user/400806/files/3a01ce34-1cb1-4ebc-ac1c-2aba11bbac20 
