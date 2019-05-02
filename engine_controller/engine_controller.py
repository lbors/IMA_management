from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import time

app = Flask(__name__)
slice_dict = {"slice":[]}
port = 8080
master_ip = '192.168.1.151'
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
    return 'Welcome to Resource and VM Management (IMA)!'

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

@app.route('/listPods', methods = ['GET'])
def list_pods_default():
    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/default/pods/")
    #resp = requests.get("http://192.168.1.151:8080/api/v1/namespaces/espaco-testes/pods/")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))
    return str(resp.status_code)

@app.route('/listPods', methods = ['POST'])
def list_pods():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()
    data = yaml.safe_load(yaml_content) # parsear pra yaml

    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['podInfo']['namespace'] + "/pods/")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))

    return str(resp.status_code)

@app.route('/getPod', methods = ['POST'])
def get_pod():
    file_name = request.data.decode('utf-8')
    print(file_name)

    # ler arquivo de parametro
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()
    data = yaml.load(yaml_content)

    resp = requests.post("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/espaco-testes/pods/" + data['podInfo']['name'])
    #resp = requests.get("http://192.168.1.151:8080/api/v1/namespaces/espaco-testes/pods/")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))
    return str(resp.status_code)

@app.route('/createPod', methods = ['POST'])
def create_pod():
    file_name = request.data.decode('utf-8')
    print(file_name)

    # ler arquivo de parametro
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    # carrega o YAML, "parseia" pra Json 
    data = yaml.load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)
    
    # curl -s http://{ip}:{porta}/api/v1/namespaces/{namespace}/pods \
    # -XPOST -H 'Content-Type: application/json' \
    # -d@{arquivo}.json 

    # curl -s http://192.168.1.151:8080/api/v1/namespaces/espaco-testes/pods -XPOST -H 'Content-Type: application/json' -d "{"apiVersion": "v1", "kind": "Pod", "metadata": {"name": "nginx", "labels": {"name": "nginx"}}, "spec": {"containers": [{"name": "nginx", "image": "nginx", "ports": [{"containerPort": 443}], "volumeMounts": [{"mountPath": "/etc/nginx/", "name": "nginx-conf"}, {"mountPath": "/usr/local/etc/nginx/ssl", "name": "ssl-certs"}]}], "volumes": [{"name": "nginx-conf", "secret": {"secretName": "nginx.conf"}}, {"name": "ssl-certs", "secret": null}]}, "secretName": "nginx-ssl-certs"}"

    resp = requests.post("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['podInfo']['namespace'] 
                            + "/pods/", data = json.dumps(json_content['podInfo']['yaml_creation']))
    return str(resp.status_code)

@app.route('/stopMonitoring/<stopMonitoring>')
def stop_monitoring():
    return 'Stopping the monitoring infrastructure'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#TODO melhorar leitura
#- listPODs precisa ser post e enviar o namespace
#- deve poder criar yamls em sequencia
#- por causa da setinha n funfa

# todo retorno printa em baixo do curl