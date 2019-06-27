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
adapter_dict = {}
adapter_dict_simulado = {
    "Telemarketing": {
        "slice-part-test-01": {
            "adapter_name": "slice-part-test-01_Telefonicas_agent",
            "port": "48697"
        },
        "slice-part-01": {
            "adapter_name": "slice-part-01_Telefonica1_agent",
            "port": "40191"
        },
        "slice-part-02": {
            "adapter_name": "slice-part-02_Telefonica2_agent",
            "port": "44681"
        }
    },
    "Clebermarketing": {
        "slice-legal": {
            "adapter_name": "legal_agent",
            "port": "555"
        }
    }
}

# port_server = 8080
# master_ip = '192.168.1.151'

def start_slice_adapter(json_content):
    global adapter_dict

    # no json_content, a variavel slice-id eh escrita com '-' (simbolo de subtracao), porem no adapter_dict usaremos '_' (underline)
    for i in json_content['dc-slice-part']:
        slice_name = i['name']
        slice_user = i['user']
        agent_name = slice_name + '_' + slice_user + '_agent'

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
        s.close()

        ######## slice-part-test-01, espaco-teste, nginx -> CHAMADA DE UM /getPod
        for j in i['vdus']: 
            if str(j['dc-vdu']['type']) == "master":
                temp_ip = str(j['dc-vdu']['ip-address']) # identifica o mestre e salva o ip nessa string
                temp_port = str(j['dc-vdu']['port'])
        # client = docker.from_env()
        # client.containers.run("agentwill:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        print("http://0.0.0.0:" + str(port) + "/setIPandPort")
        # time.sleep(3)
        master_data = temp_ip + ":" + temp_port
        if json_content['slice-id'] in adapter_dict:
            adapter_dict[json_content['slice-id']].update({ 
                    slice_name: ({
                        "adapter_name":agent_name, "port":str(port)
                    })
            })
        else:
            adapter_dict.update({
                json_content['slice-id']: {
                    slice_name: ({
                        "adapter_name":agent_name, "port":str(port)
                    })
                }
            })
        # requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
        print("The Adapter", agent_name, "has started")

@app.route('/')
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

@app.route('/listAdapters', methods = ['GET'])
def list_adapters():
    print(json.dumps(adapter_dict, indent=2))
    return 'OK'

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
    # save_dict()
    return '200'

@app.route('/createService', methods = ['POST']) 
def create_service():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    services_status = []

    for service_it in json_content['slice_parts']:
        adapter_port = adapter_dict_simulado[json_content['slice_id']][service_it['slice_part_id']]['port']
        resp = requests.post("http://0.0.0.0:" + "6661" + "/createService", data = json.dumps(service_it))
        parsed_resp = resp.content.decode('utf-8')
        services_status.append(parsed_resp)
    return ('\n'.join(services_status))

@app.route('/stopManagementAdapter')
def stop_monitoring():
    return 'Stopping the Resource and VM Management infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')




#TODO
#- deletar adapters
#- salva adapter no fim da execucao
#- yaml ou string?