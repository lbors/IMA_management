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

@app.route('/setIPandPort', methods = ['POST'])
def set_IP():
    global master_ip, master_port
    post_data = request.data.decode('utf-8')
    post_data = post_data.split(':')
    master_ip = post_data[0]
    master_port = post_data[1]

    print("IP do master: " + master_ip)
    print("Porta do master: " + master_port)
    return 'OK'

@app.route('/')
def default_options():
    return "Welcome to the Kubernetes' adapter of Resource and VM Management"



# @app.route('/getPod', methods = ['POST'])
# def get_pod():
#     file_name = request.data.decode('utf-8')
#     print(file_name)

#     # ler arquivo de parametro
#     file = open(file_name, "r")
#     yaml_content = file.read()
#     file.close()
#     data = yaml.load(yaml_content)

#     resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + data['namespace'] + "/pods/" + data['name'])

#     parsed = json.loads(resp.content)
#     print(json.dumps(parsed, indent=2))
#     return str(resp.status_code)





# @app.route('/listServices', methods = ['POST']) 
# def list_services():
#     data = request.data.decode('utf-8')
#     yaml_content = yaml.safe_load(data)
#     print(yaml_content)
#     resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + yaml_content['namespace'] + "/services/")
#     print(json.dumps(resp.json(), indent=1))
#     return (json.dumps(resp.json(), indent=2))

# @app.route('/createService', methods = ['POST'])
# def create_service():
#     data = request.data.decode('utf-8')
#     yaml_content = yaml.safe_load(data)

#     resp = requests.post("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + yaml_content['namespace'] 
#                         + "/services/", data = json.dumps(yaml_content['service_info']))
#     return (json.dumps(resp.json(), indent=2))

# @app.route('/deleteService', methods = ['POST']) 
# def delete_service():
#     data = request.data.decode('utf-8')
#     yaml_content = yaml.safe_load(data)

#     req_str = str("/api/v1/namespaces/%s/services/%s" % (yaml_content['namespace'], yaml_content['service_info']['metadata']['name']))
#     print("http://" + master_ip + ":" + str(master_port) + req_str)   # /api/v1/namespaces/{namespace}/services/{name}
#     resp = requests.delete("http://" + master_ip + ":" + str(master_port) + req_str)
#     return (json.dumps(resp.json(), indent=1))

# @app.route('/updateService', methods = ['POST']) 
# def update_service():
#     data = request.data.decode('utf-8')
#     yaml_content = yaml.safe_load(data)

#     # req_str = str("/api/v1/namespaces/%s/services/%s" % (yaml_content['namespace'], yaml_content['service_info']['metadata']['name']))
#     # print("http://" + master_ip + ":" + str(master_port) + req_str)   # PATCH /api/v1/namespa ces/{namespace}/services/{name}
#     # resp = requests.patch("http://" + master_ip + ":" + str(master_port) + req_str, data = json.dumps(yaml_content['service_info']))

#     resp = requests.patch("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + yaml_content['namespace'] 
#                         + "/services/" + str(yaml_content['service_info']['metadata']['name']), data = json.dumps(yaml_content['service_info']))
#     return (json.dumps(resp.json(), indent=1))

#     return 'OK'
# @app.route('/getService', methods = ['POST'])
# def get_service():
#     file_name = request.data.decode('utf-8')
#     print(file_name)

#     # ler arquivo de parametro
#     file = open(file_name, "r")
#     yaml_content = file.read()
#     file.close()
#     data = yaml.load(yaml_content)

#     resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + data['namespace'] + "/services/" + data['name'])

#     parsed = json.loads(resp.content)
#     print(json.dumps(parsed, indent=2))
#     return str(resp.status_code)

# slice_id, slice_part_id e namespace sao passados como argumentos
# @app.route('/listPods', methods = ['POST']) 
# def list_pods():
#     post_data = request.data.decode('utf-8') # exemplo de data: "Telemarketing, slice-part-test-01, espaco-testes"
#     post_data = post_data.split(', ')

#     resp = requests.get("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + post_data[2] + "/pods/")
#     parsed = json.loads(resp.content)
#     print(json.dumps(parsed, indent=2))
#     return (json.dumps(parsed, indent=2))

# @app.route('/deletePod', methods = ['POST']) 
# def delete_pod():
#     file_name = request.data.decode('utf-8')
#     print(file_name)

#     # ler arquivo de parametro
#     file = open(file_name, "r")
#     yaml_content = file.read()
#     file.close()

#     # carrega o YAML, "parseia" pra Json 
#     data = yaml.load(yaml_content)
#     json_content = json.dumps(data)
#     json_content = json.loads(json_content)

#     # resp = requests.delete("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['podInfo']['namespace'] + "/pods/" + data['podInfo']['name'])

#     for pod_id in json_content['pod_info']:
#         resp = requests.delete("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + pod_id['metadata']['namespace'] 
#                             + "/pods/" + pod_id['metadata']['name'])
#         print(str(resp.status_code) + "\n")

# @app.route('/createPod', methods = ['POST'])
# def create_pod():
#     file_name = request.data.decode('utf-8')
#     # print(file_name)

#     # ler arquivo de parametro
#     file = open(file_name, "r")
#     yaml_content = file.read()
#     file.close()

#     # carrega o YAML, "parseia" pra Json 
#     data = yaml.load(yaml_content)
#     json_content = json.dumps(data)
#     json_content = json.loads(json_content)
    
#     # curl -s http://{ip}:{porta}/api/v1/namespaces/{namespace}/pods \
#     # -XPOST -H 'Content-Type: application/json' \
#     # -d@{arquivo}.json 

#     for pod_id in json_content['pod_info']:
#         resp = requests.post("http://" + master_ip + ":" + str(master_port) + "/api/v1/namespaces/" + pod_id['metadata']['namespace'] 
#                             + "/pods/", data = json.dumps(pod_id))
#         print(str(resp.status_code) + "\n")

#     return 'OK'


@app.route('/listServices', methods = ['POST']) 
def list_services():
    data = request.data.decode('utf-8')
    yaml_content = yaml.safe_load(data)
    # GET /apis/apps/v1/namespaces/{namespace}/pods
    req_str = str("/api/v1/namespaces/%s/pods" % (yaml_content['namespace']))
    print("http://" + master_ip + ":" + str(master_port) + req_str)   
    resp = requests.get("http://" + master_ip + ":" + str(master_port) + req_str)
    return (json.dumps(resp.json(), indent=2))

@app.route('/deployService', methods = ['POST'])
def deploy_service():
    data = request.data.decode('utf-8')
    #yaml_content = yaml.safe_load(data)
    json_content = json.loads(data)
    #  POST /apis/apps/v1/namespaces/{namespace}/pods
    req_str = str("/api/v1/namespaces/%s/pods" % (json_content['namespace']))
    print("http://" + master_ip + ":" + str(master_port) + req_str)   
    #resp = requests.post("http://" + master_ip + ":" + str(master_port) + req_str, data = json.dumps(json_content['service_info']))
    resp = requests.post("http://" + master_ip + ":" + str(master_port) + req_str, data = json_content['service_info'])
    print(json_content['service_info'])
    return (json.dumps(resp.json(), indent=2))

@app.route('/deleteService', methods = ['POST'])
def delete_service():
    data = request.data.decode('utf-8')
    yaml_content = yaml.safe_load(data)
    #  DELETE /apis/apps/v1/namespaces/{namespace}/pods/{name}
    req_str = str("/api/v1/namespaces/%s/pods/%s" % (yaml_content['namespace'], yaml_content['service_info']['metadata']['name']))
    print("http://" + master_ip + ":" + str(master_port) + req_str)   
    resp = requests.delete("http://" + master_ip + ":" + str(master_port) + req_str)
    return (json.dumps(resp.json(), indent=2))
    
@app.route('/updateService', methods = ['POST'])
def update_service():
    data = request.data.decode('utf-8')
    yaml_content = yaml.safe_load(data)
    json_content = json.loads(data)
    #  PATCH /apis/apps/v1/namespaces/{namespace}/pods/{name}
    req_str = str("/apis/apps/v1/namespaces/%s/pods/%s" % (yaml_content['namespace'], yaml_content['service_info']['metadata']['name']))
    print("http://" + master_ip + ":" + str(master_port) + req_str)   
    head = {"Content-Type": "application/strategic-merge-patch+json"}
    print(json.dumps(json_content['service_info']))
    resp = requests.patch("http://" + master_ip + ":" + str(master_port) + req_str, data = json.dumps(json_content['service_info']), headers = head)
    return (json.dumps(resp.json(), indent=2))

# @app.route('/updateScale', methods = ['POST'])
# def update_scale():
#     data = request.data.decode('utf-8')
#     yaml_content = yaml.safe_load(data)
#     #  PATCH /apis/apps/v1/namespaces/{namespace}/pods/{name}/scale
#     req_str = str("/apis/apps/v1/namespaces/%s/pods/%s/scale" % (yaml_content['namespace'], yaml_content['service_info']['metadata']['name']))
#     print("http://" + master_ip + ":" + str(master_port) + req_str)   
#     resp = requests.patch("http://" + master_ip + ":" + str(master_port) + req_str, data = json.dumps(yaml_content['service_info']))
#     return (json.dumps(resp.json(), indent=2))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')



#TODO 
#- ATUALIZAR FUNCOES (exemplo: ListServices recebe nome de arquivo como parametro, replicaScale nao funciona corretamente, etc)