from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import time

app = Flask(__name__)
master_port = 8080
master_ip = '192.168.1.151'

@app.route('/setIPandPort', methods = ['POST'])
def set_IP():
    global master_ip, port
    data = request.data.decode('utf-8')
    data = data.split(':')
    master_ip = data[0]
    master_port = data[1]

    print("IP do master: " + master_ip)
    print("Porta do master: " + master_port)
    return 'OK'


@app.route('/createService', methods = ['POST'])
def create_service():
    yaml_content = request.data.decode('utf-8')
    # print("data sem parse: \n" + yaml_content)

    # carrega o YAML, "parseia" pra Json 
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    # print("data pos parse: \n")
    # json_content.dumps()
    for service_id in json_content['service_info']:
        time.sleep(3)
        print("REQUISICAO = http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + json_content['namespace'] 
                            + "/services/")
        resp = requests.post("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + json_content['namespace'] 
                            + "/services/", data = json.dumps(service_id))
        print(str(resp.headers) + "\n")
    return 'OK'


@app.route('/listPods', methods = ['GET']) 
def list_pods_default():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/default/pods/")
    parsed = json.loads(resp.content)
    return (json.dumps(parsed, indent=2))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='6661')

