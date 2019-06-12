from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import socket
import time
from subprocess import call 

app = Flask(__name__)
adapter_dict = {"adapters":[]}
# port_server = 8080
# master_ip = '192.168.1.151'

@app.route('/createPod', methods = ['POST']) 
def create_pod():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    # carrega o YAML, "parseia" pra Json 
    data = yaml.load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    for adapter_iterator in adapter_dict['adapters']:
        if adapter_iterator['slice_id'] == json_content['slice_id']:
            for slice_part_it in adapter_iterator['parts']:
                if slice_part_it['slice_part_id'] == json_content['slice_part_id']:
                    resp = requests.post("http://0.0.0.0:" + slice_part_it['port'] + "/createPod", data = request.data)
                    parsed = json.loads(resp.content)
                    # print(json.dumps(parsed, indent=2))
                    return 'OK'
    return 'Adapter not found'

# slice_id, slice_part_id e namespace sao passados como argumentos
@app.route('/listPods', methods = ['POST']) 
def list_pods():
    post_data = request.data.decode('utf-8') # exemplo de data: "Telemarketing;slice-part-test-01;espaco-testes"
    splitted_data = post_data.split(';')    
    # print(data)

    for adapter_iterator in adapter_dict['adapters']:
        if adapter_iterator['slice_id'] == splitted_data[0]:
            for slice_part_it in adapter_iterator['parts']:
                if slice_part_it['slice_part_id'] == splitted_data[1]:
                    resp = requests.post("http://0.0.0.0:" + slice_part_it['port'] + "/listPods", data = post_data)
                    parsed = json.loads(resp.content)
                    print(json.dumps(parsed, indent=2))
                    return 'OK'
    # resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/pods/")
    return 'Adapter not found'

def start_slice_adapter(json_content):
    global adapter_dict
    
    #Start container for the IMA Agents/Adapters
    adapter_dict["adapters"].append({"slice_id":json_content['slice-id'],"parts":[]})
    # no json_content, a variavel slice-id eh escrita com '-' (simbolo de subtracao), porem no adapter_dict usaremos '_' (underline)
    
    


@app.route('/')
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

@app.route('/listAdapters', methods = ['GET'])
def list_adapters():
    print(json.dumps(adapter_dict, indent=2))
    return 'OK'

@app.route('/stopSlicePart', methods = ['POST'])
def delete_adapter():
    post_data = request.data.decode('utf-8')
    splitted_data = post_data.split(';')

    for adapter_iterator in adapter_dict['adapters']:
        if adapter_iterator['slice_id'] == splitted_data[0]:
            for slice_part_it in adapter_iterator['parts']:
                if slice_part_it['slice_part_id'] == splitted_data[1]:
                    client = docker.from_env()
                    container = client.containers.get(slice_part_it['adapter_name'])
                    container.stop()
                    container.remove()
                    del slice_part_it
                    return 'OK'
    return 'Adapter not found'

@app.route('/startManagement', methods = ['POST'])
def start_management():
    file_name = request.data.decode('utf-8')  # 
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    json_content = json.dumps(yaml.safe_load(yaml_content))
    json_content = json.loads(json_content)

    start_slice_adapter(json_content)
    list_adapters()
    return '200'


@app.route('/stopManagement', methods = ['POST'])
def stop_management():
    post_data = request.data.decode('utf-8') # exemplo de entrada: "Telefonica"

    for adapter_iterator in adapter_dict['adapters']:
        if adapter_iterator['slice_id'] == post_data:
            for slice_part_it in adapter_iterator['parts']:
                client = docker.from_env()
                container = client.containers.get(slice_part_it['adapter_name'])
                container.stop()
                container.remove()
                del slice_part_it 
            adapter_dict['adapters'].remove(adapter_iterator)
            print('The slice ' + post_data + ' has been deleted.')
            return '200'
    print('Adapter not found')
    return '400'

# @app.route('/updateManagement', methods = ['POST'])
# def stop_management():
#     post_data = request.data.decode('utf-8') # exemplo de entrada: "Telefonica"

#     for adapter_iterator in adapter_dict['adapters']:
#         if adapter_iterator['slice_id'] == post_data:
#             for slice_part_it in adapter_iterator['parts']:
#                 client = docker.from_env()
#                 container = client.containers.get(slice_part_it['adapter_name'])
#                 container.stop()
#                 container.remove()
#                 del slice_part_it 
#             adapter_dict['adapters'].remove(adapter_iterator)
#             print('The slice ' + post_data + ' has been deleted.')
#             return '200'
#     print('Adapter not found')
#     return '400'

def stop_ma():
    return 'Stopping the Resource and VM Management infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')




#TODO
#- perguntar sobre retorno (a resposta eu que configuro? tem como voltar tanto uma resposta como um numero)
#- salva adapter no fim da execucao