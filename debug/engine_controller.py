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

adapter_dict = {}

def save_dict():
    #filename = ""
    write_file = open("global_dict.json", 'w')
    json.dump(adapter_dict, write_file)
    write_file.close() 

""" @app.before_first_request
def load_dict():
    global adapter_dict
    try:
        file = open("global_dict.json", "r")
        data = file.read()
        file.close()
        adapter_dict = json.loads(data)
    except FileNotFoundError:
        print ('File "global_dict.json" does not exist. Resuming execution.')   
    except AttributeError: 
        print ('File "global_dict.json" is not a valid Json file. Resuming execution with a empty dict.')  
 """

def reset_dict():
    global adapter_dict
    adapter_dict = {}
    save_dict()


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
        requests.post("http://0.0.0.0:" + "6661" + "/setIPandPort", data = master_data)
        print("The Adapter", agent_name, "has started")

def start_slice_adapter_ssh(json_content):
    global adapter_dict

    for i in json_content['dc-slice-part']:
        if i['VIM']['VIM_Type_access'] == 'SSH':
            slice_name = i['name']
            slice_user = i['user']
            agent_name = slice_name + '_' + slice_user + '_agent_ssh'
            ssh_ip = i['VIM']['IP']
            ssh_port = i['VIM']['port']
            ssh_user = i['VIM']['user']
            ssh_pass = i['VIM']['password']
            master_ip = i['vdus'][0]['dc-vdu']['ip-address']

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', 0))
            port = s.getsockname()[1]
            s.close()

            # client = docker.from_env()
            # client.containers.run("adapter_ssh:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
            print("http://0.0.0.0:" + str(port) + "/setSSH")
            # time.sleep(3)
            master_data = ssh_ip + ":" + ssh_port + ":" + ssh_user + ":" + ssh_pass + ":" + str(port) + ":" + master_ip

            adapter_dict[json_content['slice-id']][slice_name]['adapter_ssh_name'] = agent_name
            adapter_dict[json_content['slice-id']][slice_name]['adapter_ssh_port'] = str(port)
            adapter_dict[json_content['slice-id']][slice_name]['ssh_ip'] = str(ssh_ip)
            adapter_dict[json_content['slice-id']][slice_name]['ssh_port'] = str(ssh_port)
            adapter_dict[json_content['slice-id']][slice_name]['ssh_user'] = str(ssh_user)
            adapter_dict[json_content['slice-id']][slice_name]['ssh_pass'] = str(ssh_pass)
            adapter_dict[json_content['slice-id']][slice_name]['master_ip'] = str(master_ip)
          
            # requests.post("http://0.0.0.0:" + str(port) + "/setSSH", data = master_data)
            requests.post("http://0.0.0.0:" + "1010" + "/setSSH", data = master_data)
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
    json_content = json.dumps(yaml.safe_load(request.data.decode('utf-8')))
    json_content = json.loads(json_content)

    start_slice_adapter(json_content)
    print("START: ///////////////////////////////////////////////////////qqq")
    print(json.dumps(adapter_dict, indent=2))
    start_slice_adapter_ssh(json_content)
    print("START SSH: ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    print(json.dumps(adapter_dict, indent=2))
    save_dict()
    return str(json.dumps(adapter_dict, indent=2))

@app.route('/deployService', methods = ['POST']) 
def create_service():
    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)
    services_status = []

    slice_id = json_content['slices']['id']
    for slices_iterator in json_content['slices']['slice-parts']:
        # pra cada slice_part do yaml vai adicionar N servicos, mas em apenas UM namespace
        adapter_port = adapter_dict[slice_id][str(slices_iterator['name'])]['adapter_ssh_port']

        print("slices_iterator:" + str(slices_iterator)) 
        for service_it in slices_iterator['vdus']:
            print("service_it:" + str(service_it)) 
            # resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/createService", data = json.dumps(service_it['commands']))
            resp = requests.post("http://0.0.0.0:" + "1010" + "/createService", data = json.dumps(service_it['commands']))
        # parsed_resp = resp.content.decode('utf-8')
        # services_status.append(parsed_resp)
    # return ('\n'.join(services_status))
    return 'OK'

@app.route('/stopManagementAdapter')
def stop_monitoring():
    return 'Stopping the Resource and VM Management infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')




#TODO
#- deletar adapters
#- salva adapter no fim da execucao
#- yaml ou string?