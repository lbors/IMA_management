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

# @app.route('/getPod', methods = ['POST']) 
# def get_pod():
#     post_data = request.data.decode('utf-8') # exemplo de data: "Telemarketing;slice-part-test-01;espaco-testes;nginx"
#     splitted_data = post_data.split(';')    
#     # print(data)

#     for adapter_iterator in adapter_dict['adapters']:
#         if adapter_iterator['slice_id'] == splitted_data[0]:
#             for slice_part_it in adapter_iterator['parts']:
#                 if slice_part_it['slice_part_id'] == splitted_data[1]:
#                     yaml = str('---\nnamespace: ' + splitted_data[2] + '\nname: ' + splitted_data[3])
#                     resp = requests.post("http://0.0.0.0:" + slice_part_it['port'] + "/listPods", data = yaml)
#                     parsed = json.loads(resp.content)
#                     print(json.dumps(parsed, indent=2))
#                     return 'OK'
#     # resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/pods/")
#     return 'Adapter not found'


# slice_id, slice_part_id e namespace sao passados como argumentos
# @app.route('/listPods', methods = ['POST']) 
# def list_pods():
    # post_data = request.data.decode('utf-8') # exemplo de data: "Telemarketing;slice-part-test-01;espaco-testes"
    # splitted_data = post_data.split(';')    
    # # print(data)

    # for adapter_iterator in adapter_dict['adapters']:
    #     if adapter_iterator['slice_id'] == splitted_data[0]:
    #         for slice_part_it in adapter_iterator['parts']:
    #             if slice_part_it['slice_part_id'] == splitted_data[1]:
    #                 resp = requests.post("http://0.0.0.0:" + slice_part_it['port'] + "/listPods", data = post_data)
    #                 parsed = json.loads(resp.content)
    #                 print(json.dumps(parsed, indent=2))
    #                 return 'OK'
    # # resp = requests.get("http://" + master_ip + ":" + str(port) + "/api/v1/namespaces/" + data['namespace'] + "/pods/")
    # return 'Adapter not found'

def start_slice_adapter(json_content):
    global adapter_dict
    
    #Start container for the IMA Agents/Adapters
    adapter_dict["adapters"].append({"slice_id":json_content['slice-id'],"parts":[]})
    # no json_content, a variavel slice-id eh escrita com '-' (simbolo de subtracao), porem no adapter_dict usaremos '_' (underline)
    
    for i in json_content['dc-slice-part']:
        slice_name = i['name']
        slice_user = i['user']
        agent_name = slice_name + '_' + slice_user + '_agent'
        # print ('Nome da slice:' + str(slice_name))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
        s.close()
        # SALVAR: slice_part_id, slice port
        ######## slice-part-test-01, espaco-teste, nginx -> CHAMADA DE UM /getPod
        for j in i['vdus']: 
            if str(j['dc-vdu']['type']) == "master":
                temp_ip = str(j['dc-vdu']['ip-address']) # identifica o mestre e salva o ip nessa string
                temp_port = str(j['dc-vdu']['port'])

        client = docker.from_env()
        client.containers.run("agentwill:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        print("http://0.0.0.0:" + str(port) + "/setIPandPort")
        time.sleep(3)
        master_data = temp_ip + ":" + temp_port
        for k in adapter_dict['adapters']:
            # print(k)
            if k['slice_id'] == json_content['slice-id']:
                k['parts'].append({"slice_part_id":slice_name,"adapter_name":agent_name,"port":str(port)})
        # adapter_dict["adapters"].append({"slice_part_id":slice_name,"adapter_name":agent_name,"port":str(port)})

        # print(json.dumps(adapter_dict, indent=2))

        requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
        print("The Adapter", agent_name, "has started")

    # adapter_dict["adapters"].append(})

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
    file_name = request.data.decode('utf-8')
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

@app.route('/updateManagement', methods = ['POST'])
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

def stop_ma():
    return 'Stopping the Resource and VM Management infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')




#TODO
#- deletar adapters
#- salva adapter no fim da execucao