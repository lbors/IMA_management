from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json

app = Flask(__name__)
master_port = 8080
master_ip = '1.1.1.1'

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

@app.route('/listPods', methods = ['GET']) 
def list_pods_default():
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/default/pods/")
    parsed = json.loads(resp.content)
    return (json.dumps(parsed, indent=2))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='6661')
