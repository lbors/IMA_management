from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import time

app = Flask(__name__)
master_port = 8080
master_ip = '1.1.1.1'

@app.route('/setInitialConfig', methods = ['POST'])
def set_config():
    global master_ip, master_port
    post_data = request.data.decode('utf-8')
    post_data = post_data.split(':')
    master_ip = post_data[0]
    master_port = post_data[1]
    # FAZER  /auth  ???????????????
    print("IP do master: " + master_ip + "\tPorta do master: " + master_port)
    return 'OK'

# {
#   "username": "hannibal", 
#   "password": "xxxx",
#   "serveraddress": "https://index.docker.io/v1/"
# }

@app.route('/getNodes', methods = ['GET'])
def get_nodes():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/nodes")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))
    return str(resp.status_code)

@app.route('/inspectSwarm', methods = ['GET'])
def inspect_swarm():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/swarm")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))
    return str(resp.status_code)

@app.route('/listServices', methods = ['GET']) 
def list_services():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()
    data = yaml.safe_load(yaml_content) # parsear pra yaml

    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + data['namespace'] + "/services/")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))

    return str(resp.status_code)

@app.route('/deployService', methods = ['POST'])
def deploy_service():
    yaml_content = request.data.decode('utf-8')

    # carrega o YAML, "parseia" pra Json 
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    service_info = []

    for service_id in json_content['service_info']:
        resp = requests.post("http://" + master_ip + ":" + str(master_port) + " /services/create", data = json.dumps(service_id))
        r = json.loads(resp.content.decode('utf-8'))
        if r["status"] == "Failure":
            try:
                obj = "Service " + service_id['metadata']['name'] + " could not be initialized. Error " + str(r["code"]) + ": " + r["message"]
            except Exception:
                obj = "A nameless service could not be initialized. Error " + str(r["code"]) + ": " + r["message"]
        else:
            obj = "Service " + service_id['metadata']['name'] + " initialized successfully."
        service_info.append(obj)
    return str(service_info)

@app.route('/')
def default_options():
    return "Welcome to the Swarm's adapter of Resource and VM Management! This is in early stage."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')