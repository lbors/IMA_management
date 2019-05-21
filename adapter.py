from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json

app = Flask(__name__)
port = 8080
master_ip = '1.1.1.1'

@app.route('/setIPandPort', methods = ['POST'])
def set_IP():
    global master_ip
    data = request.data.decode('utf-8')
    master_ip = data

@app.route('/')
def default_options():
    return 'Welcome to the adapter X of Resource and VM Management'

# sem argumentos, o metodo lista os pods do namespace DEFAULT
@app.route('/listPods', methods = ['GET']) 
def list_pods_default():
    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/default/pods/")
    #resp = requests.get("http://192.168.1.151:8080/api/v1/namespaces/espaco-testes/pods/")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))
    return str(resp.status_code)

# namespace é passado como argumento 
@app.route('/listPods', methods = ['POST']) 
def list_pods():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()
    data = yaml.safe_load(yaml_content) # parsear pra yaml

    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/pods/")
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

    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/pods/" + data['name'])

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

    for pod_id in json_content['pod_info']:
        resp = requests.post("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + pod_id['metadata']['namespace'] 
                            + "/pods/", data = json.dumps(pod_id))
        print(str(resp.status_code) + "\n")

    return 'OK'


@app.route('/deletePod', methods = ['POST']) 
def delete_pod():
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

    # resp = requests.delete("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['podInfo']['namespace'] + "/pods/" + data['podInfo']['name'])

    for pod_id in json_content['pod_info']:
        resp = requests.delete("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + pod_id['metadata']['namespace'] 
                            + "/pods/" + pod_id['metadata']['name'])
        print(str(resp.status_code) + "\n")

    return 'OK'

@app.route('/listServices', methods = ['POST']) 
def list_services():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()
    data = yaml.safe_load(yaml_content) # parsear pra yaml

    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/services/")
    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))

    return str(resp.status_code)

@app.route('/createService', methods = ['POST'])
def create_service():
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

    for service_id in json_content['service_info']:
        resp = requests.post("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + json_content['namespace'] 
                            + "/services/", data = json.dumps(service_id))
        print(str(resp.status_code) + "\n")

    return 'OK'

@app.route('/getService', methods = ['POST'])
def get_service():
    file_name = request.data.decode('utf-8')
    print(file_name)

    # ler arquivo de parametro
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()
    data = yaml.load(yaml_content)

    resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/services/" + data['name'])

    parsed = json.loads(resp.content)
    print(json.dumps(parsed, indent=2))
    return str(resp.status_code)


@app.route('/deleteService', methods = ['POST']) 
def delete_service():
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

    for service_id in json_content['service_info']:
        resp = requests.delete("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + json_content['namespace'] 
                            + "/services/" + service_id['metadata']['name'])
        print(str(resp.status_code) + "\n")

    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')



#TODO 
#- melhorar leitura
#- deixar bonito???????