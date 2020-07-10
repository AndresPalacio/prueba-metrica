#!/usr/bin/env python3
import boto3
import psutil
import requests
import datetime

_METADATAURL = 'http://169.254.169.254/latest/meta-data'  # where to obtain instance metadata ...

cw = boto3.client('cloudwatch', region_name='us-east-1')
currMetrics = []


def appendMetrics(CurrentMetrics, Dimensions, Name, Unit, Value):
    metric = {'MetricName': Name
        , 'Dimensions': Dimensions
        , 'Unit': Unit
        , 'Value': Value
              }
    CurrentMetrics.append(metric)


def memProcessChromeDrive():
    return len([p.info['pid'] for p in psutil.process_iter(attrs=['pid','name','create_time'])
             if 'chrome' in p.info['name']
              if(datetime.datetime.now() - datetime.datetime.fromtimestamp(p.info['create_time'])).seconds % 3600 / 60.0 >= 1])


if __name__ == '__main__':
    print(memProcessChromeDrive())
    instance_id = requests.get(_METADATAURL + '/instance-id').text
    instance_type = requests.get(_METADATAURL + '/instance-type').text
    dimensions = [{'Name': 'InstanceId', 'Value': instance_id}, {'Name': 'InstanceType', 'Value': instance_type}]
    appendMetrics(currMetrics, dimensions, Name='ProcessChromedriver', Value=memProcessChromeDrive(), Unit='Count')
    response = cw.put_metric_data(MetricData=currMetrics, Namespace='CustomMetricChromeDrive')
