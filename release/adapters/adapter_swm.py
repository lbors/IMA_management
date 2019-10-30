from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import time

# HABILITAR API DO SWARM:
# 1- corrigir data e hora do master (precisa de confirmacao)
    # sudo unlink /etc/localtime
    # sudo ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
    # timedatectl 
# 2- editar arquivo no leader
    # sudo vim /lib/systemd/system/docker.service
        # ExecStart=/usr/bin/dockerd -H fd:// -H=tcp://0.0.0.0:5555 [qualquer porta que quiser abrir]
    # sudo systemctl reload
    # sudo systemctl daemon-reload
    # sudo service docker restart
    # sudo docker ps

app = Flask(__name__)
master_port = -1
master_ip = 'null'

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

@app.route('/getNodes', methods = ['GET'])
def get_nodes():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/nodes")
    parsed = json.loads(resp.content)
    return str(json.dumps(parsed, indent=2))

@app.route('/inspectSwarm', methods = ['GET'])
def inspect_swarm():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/swarm")
    parsed = json.loads(resp.content)
    return str(json.dumps(parsed, indent=2))

@app.route('/listServices', methods = ['GET']) 
def list_services():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/services")
    parsed = json.loads(resp.content)
    return str(json.dumps(parsed, indent=2))

@app.route('/deployService', methods = ['POST'])
def deploy_service():
    data = request.data.decode('utf-8')
    json_content = json.loads(data)

    resp = requests.post("http://" + master_ip + ":" + str(master_port) + "/services/create", data = json.dumps(json_content))
    parsed = json.loads(resp.content)
    print(str(json.dumps(parsed, indent=2)))
    return str(parsed)

@app.route('/deleteService', methods = ['POST'])
def delete_service():
    data = request.data.decode('utf-8')
    yaml_content = yaml.safe_load(data)

    resp = requests.delete("http://" + master_ip + ":" + str(master_port) + "/services/" + yaml_content['service-id'])
    # parsed = json.loads(resp.content)
    # print(str(json.dumps(parsed, indent=2)))
    # print(str(resp.content))
    return '200'

@app.route('/')
def default_options():
    return "Welcome to the Swarm's adapter of Resource and VM Management!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')