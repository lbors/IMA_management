from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import time

app = Flask(__name__)
slice_dict = {"slice":[]}
port = 2000
slice_provider_ip = '200.136.191.58'

def start_slice_aggregator(slice_id):
    global slice_dict
    global port
    global slice_provider_ip
    
    #Start container for the Slice Aggregator Component
    aggregator_name = slice_id + '_slice_aggregator'

    client = docker.from_env()
    client.containers.run("sliceaggregator:latest", detach=True, name=aggregator_name, ports={'1010/tcp': ('localhost', port)})
    #slice_provider_ip is related to where the RABBITMQ and INFLUXDB are running
    time.sleep(10)
    data = "{'slice_id':'" + slice_id + "','slice_provider_ip':'" + slice_provider_ip + "'}"
    print(json.dumps(data,separators=(',',':')))
    requests.post("http://0.0.0.0:" + str(port) + "/startMonitoring", data = json.dumps(data))

    slice_dict["slice"].append({"slice_id":slice_id,"monitoring_agg_ip":"0.0.0.0","monitoring_agg_port":str(port),"monitoring_agg_name":aggregator_name,"slice_part":[]})
    port = port + 1

def start_slice_adapter(json_content):
    global slice_dict
    global port
    
    #Start container for the IMA Agents/Adapters
    for i in range(len(json_content['slice']['vim'])):
        slice_id = json_content['slice']['id']
        slice_part_id = json_content['slice']['vim'][i]['slice-vim']['name']
        monitoring_tool = json_content['slice']['vim'][i]['slice-vim']['monitoring-parameters']['tool']
        monitoring_ip = json_content['slice']['vim'][i]['slice-vim']['monitoring-parameters']['measurements-db-ip']
        monitoring_port = json_content['slice']['vim'][i]['slice-vim']['monitoring-parameters']['measurements-db-port']
        monitoring_interval = json_content['slice']['vim'][i]['slice-vim']['monitoring-parameters']['granularity-secs']

        agent_name = slice_id + '_' + slice_part_id + '_agent'
        if monitoring_tool == 'prometheus':
            client = docker.from_env()
            client.containers.run("agentprom:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        
        metrics = list()
        for j in range(len(json_content['slice']['vim'][i]['slice-vim']['monitoring-parameters']['metrics'])):
            metrics.append(json_content['slice']['vim'][i]['slice-vim']['monitoring-parameters']['metrics'][j]['metric']['name'])

        time.sleep(5)
        #print("PRINTING METRICS", metrics)
        data = "{'slice_id':'" + slice_id + "','slice_part_id':'" + slice_part_id + "','monitoring_ip':'" + str(monitoring_ip) + "','monitoring_port':'" + str(monitoring_port) + "','monitoring_interval':'" + str(monitoring_interval) + "','monitoring_tool':'" + str(monitoring_tool) + "','metrics':" + str(metrics) + ",'slice_provider_ip':'" + slice_provider_ip + "'}"
        print(json.dumps(data,separators=(',',':')))
        requests.post("http://0.0.0.0:" + str(port) + "/startMonitoring", data = json.dumps(data))
       
        for i in range(len(slice_dict["slice"])):
            if slice_dict["slice"][i]["slice_id"] == slice_id:
               slice_dict["slice"][i]["slice_part"].append({"slice_part_id":slice_part_id,"monitoring_adapter_ip":"0.0.0.0","monitoring_adapter_port":str(port),"monitoring_adapter_name":agent_name,"monitoring_tool":monitoring_tool})

        port = port + 1 
    
        print("The Adapter ", agent_name, " has started")

@app.route('/')
def default_options():
    return 'Welcome to Monitoring Engine Controller'

@app.route('/startMonitoring', methods = ['POST'])
def start_monitoring():
    #print(request.headers)
    file_name = request.data.decode('utf-8')
    print(file_name)
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    json_content = json.dumps(yaml.safe_load(yaml_content))
    json_content = json.loads(json_content)
    slice_id = json_content['slice']['id']

    start_slice_aggregator(slice_id)
    start_slice_adapter(json_content)
    # /home/williamgdo/Documentos/git/IMA_management/yamlFiles/slice1.yaml


@app.route('/stopMonitoring/<stopMonitoring>')
def stop_monitoring():
    return 'Stoping the monitoring infrastructure'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

