#!/usr/bin/env python3
import json
import boto3
from itertools import islice

_METADATAURL = 'http://169.254.169.254/latest/meta-data'  # where to obtain instance metadata ...




def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k for k in islice(it, SIZE)}


if __name__ == '__main__':
    ec2_client = boto3.client('ec2',region_name='us-east-1')
    CW_client = boto3.client('cloudwatch', region_name='us-east-1')
    regions = ['us-east-1']
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'instance-state-name',
                 'Values': ['running']
                 }
            ]
        )
    DATA = [];
    CPUUtilization_template = '["AWS/EC2","CPUUtilization","InstanceId","{}"]'
    EBSIOBalance_template = '["AWS/EC2","EBSIOBalance%" ,"InstanceId","{}"]'
    CPUUtilization_array = []
    EBSIOBalance_array = []
    # creacion de la lista, para acceder a las instancias
    instancesnew = list(map(lambda x: x.id,instances.all()))
    element = 1
    for i in chunks(instancesnew,2):
        element += 1
        valor1 = 0 if element % 2 == 0 else 12
        print('ingreso')
        for d in i:
            CPUUtilization_array.append(CPUUtilization_template.format(d));
            EBSIOBalance_array.append(EBSIOBalance_template.format(d));
            print(CPUUtilization_array)
        print("primer for")
        CPUUtilization_string = ",".join(CPUUtilization_array);
        CPUUtilization_array =[];
        EBSIOBalance_string = ",".join(EBSIOBalance_array);
        EBSIOBalance_array = [];
        CPUUtilization_instances = r'{"type":"metric","x":'+str(valor1)+r',"y":24,"width":12,"height":6,"properties":{"metrics":[' + CPUUtilization_string + r'],"view":"timeSeries","stacked":false,"region":"us-east-1","stat":"Average","period":5,"title":"WebServers - CPU"}}'
        EBSIOBalance_instances = r'{"type":"metric","x":'+str(valor1)+r',"y":24,"width":12,"height":6,"properties":{"metrics":[' + EBSIOBalance_string + r'],"view":"timeSeries","stacked":false,"region":"us-east-1","stat":"Average","period":5,"title":"OTRO"}}'
        DATA.append(CPUUtilization_instances)
        DATA.append(EBSIOBalance_instances)

  
  
    data_string = ",".join(DATA);
    DashboardBody='{"widgets":[' + data_string + ']}'
    print(DashboardBody)
    
    
    response = CW_client.put_dashboard(DashboardName='test2', DashboardBody='{"widgets":[' + data_string + ']}')
