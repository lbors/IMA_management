from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import time

app = Flask(__name__)
master_port = 8080
master_ip = '200.18.102.80'

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

    # carrega o YAML, "parseia" pra Json 
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    service_info = []

    for service_id in json_content['service_info']:
        time.sleep(3)
        resp = requests.post("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + json_content['namespace'] 
                            + "/services/", data = json.dumps(service_id))
        r = json.loads(resp.content.decode('utf-8'))
        if r["status"] == "Failure":
            try:
                obj = "Service " + service_id['metadata']['name'] + " could not be initialized. Error " + str(r["code"]) + ": " + r["message"]
            except Exception as e:
                obj = """A nameless service could not be initialized. Error """ + str(r["code"]) + ": " + r["message"]
        else:
            obj = "Service " + service_id['metadata']['name'] + " initialized successfully."

        service_info.append(obj)
    return str(service_info)

@app.route('/listPods', methods = ['GET']) 
def list_pods_default():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/default/pods/")
    parsed = json.loads(resp.content)
    return (json.dumps(parsed, indent=2))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='6661')

