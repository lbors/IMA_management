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

def save_dict():
    #filename = ""
    write_file = open("global_dict.json", 'w')
    json.dump(adapter_dict, write_file)
    write_file.close() 

@app.before_first_request
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

def reset_dict():
    global adapter_dict
    adapter_dict = {}
    save_dict()

def start_slice_adapter(json_content):
    global adapter_dict

    for i in range(len(json_content['slice']['slice-parts'])): 
    # precisa percorrer todos slice parts do yaml para iniciar
        # print(str("slice " + str(i) + " = " + str(json_content['slice']['slice-parts'][i]))) 
        temp_ip = str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vim-ref']['ip-api'])
        slice_name = json_content['slice']['slice-parts'][i]['dc-slice-part']['name']
        
        if temp_ip != "null":
            temp_port = json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vim-ref']['port-api']
            master_data = temp_ip + ":" + str(temp_port)

            agent_name = slice_name + '_adapter_api'

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', 0))
            port = s.getsockname()[1]
            s.close()
            
            client = docker.from_env()
            client.containers.run("adapterk8s:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
            time.sleep(3)

            if json_content['slice']['id'] in adapter_dict:
                adapter_dict[json_content['slice']['id']].update({ 
                        slice_name: ({
                            "adapter_api_name":agent_name, "port":str(port)
                        })
                })
            else:
                adapter_dict.update({
                    json_content['slice']['id']: {
                        slice_name: ({
                            "adapter_api_name":agent_name, "port":str(port)
                        })
                    }
                })
            # print("http://0.0.0.0:" + str(port) + "/setIPandPort")
            requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
            print("The Adapter", agent_name, "has started")
        else:
            if json_content['slice']['id'] in adapter_dict:
                adapter_dict[json_content['slice']['id']].update({ 
                        slice_name: ({
                            "adapter_api_name":"null"
                        })
                })
            else:
                adapter_dict.update({
                    json_content['slice']['id']: {
                        slice_name: ({
                            "adapter_api_name":"null"
                        })
                    }
                })


def start_slice_adapter_ssh(json_content):
    global adapter_dict

    for i in range(len(json_content['slice']['slice-parts'])):
        ssh_ip = str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vim-ref']['ip-ssh'])
        slice_name = json_content['slice']['slice-parts'][i]['dc-slice-part']['name']
        
        if ssh_ip != "null":
            agent_name = slice_name + '_adapter_ssh'
            ssh_port = json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vim-ref']['port-ssh']
            ssh_user = json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vim-credential']['user-ssh']
            ssh_pass = json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vim-credential']['password-ssh']

            master_ip = "null"

            for j in range(len(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'])): 
            # for para identificar o master sequencialmente
                print(str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'][j]))
                if str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'][j]['vdu']['type']) == "master": # um campo type identifica o mestre 
                    master_ip = str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'][j]['vdu']['ip']) 

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', 0))
            port = s.getsockname()[1]
            s.close()

            client = docker.from_env()
            client.containers.run("adapter_ssh:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
            time.sleep(3)

            adapter_dict[json_content['slice']['id']][slice_name]['adapter_ssh_name'] = agent_name
            adapter_dict[json_content['slice']['id']][slice_name]['adapter_ssh_port'] = str(port)
            adapter_dict[json_content['slice']['id']][slice_name]['ssh_ip'] = str(ssh_ip)
            adapter_dict[json_content['slice']['id']][slice_name]['ssh_port'] = str(ssh_port)
            adapter_dict[json_content['slice']['id']][slice_name]['ssh_user'] = str(ssh_user)
            adapter_dict[json_content['slice']['id']][slice_name]['ssh_pass'] = str(ssh_pass)
            adapter_dict[json_content['slice']['id']][slice_name]['master_ip'] = str(master_ip)
            
            master_data = ssh_ip + ":" + str(ssh_port) + ":" + ssh_user + ":" + ssh_pass + ":" + str(port) + ":" + master_ip
            # print("http://0.0.0.0:" + str(port) + "/setSSH")
            requests.post("http://0.0.0.0:" + str(port) + "/setSSH", data = master_data)
            print("The Adapter", agent_name, "has started")
        else:
            adapter_dict[json_content['slice']['id']][slice_name]['adapter_ssh_name'] = "null"

@app.route('/')
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

@app.route('/listAdapters', methods = ['GET'])
def list_adapters():
    # print(json.dumps(adapter_dict, indent=2))
    return str(json.dumps(adapter_dict, indent=2))
    
@app.route('/updateManagement', methods = ['POST'])
def update_management():
    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    if json_content['flag'] == "append":
        start_slice_adapter(json_content)
        save_dict()
        return str(json.dumps(adapter_dict, indent=2))
    elif json_content['flag'] == "delete":  
        client = docker.from_env()
        container = client.containers.get(str(json_content['slice-part-id']))
        container.stop()
        container.remove()
        adapter_dict[json_content['slice-id']].pop(json_content['slice-part-id'])
        save_dict()
        return str(json.dumps(adapter_dict, indent=2))
    else: 
        return 'Error: The yaml sent has a invalid flag.'
    

@app.route('/necos/ima/start_management', methods = ['POST'])
def start_management():
    json_content = json.dumps(yaml.safe_load(request.data.decode('utf-8')))
    json_content = json.loads(json_content)

    start_slice_adapter(json_content)
    start_slice_adapter_ssh(json_content)
    # list_adapters()
    save_dict()
    return str(json.dumps(adapter_dict, indent=2))

@app.route('/stopManagement', methods = ['POST'])
def stop_management():
    post_data = request.data.decode('utf-8') # exemplo de entrada: "Telefonica"

    for slice_part in adapter_dict[post_data]:
        client = docker.from_env()
        container = client.containers.get(slice_part)
        container.stop()
        container.remove()
    adapter_dict.pop(post_data)
    save_dict()
    return str('The slice ' + post_data + ' has been deleted.')

# SERVICES ########################################################################

@app.route('/necos/ima/deploy_service', methods = ['POST']) 
def create_service():
    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)
    services_status = []

    slice_id = json_content['slices']['sliced']['id']
    for slices_iterator in json_content['slices']['sliced']['slice-parts']:
        # pra cada slice_part do yaml vai adicionar N servicos, mas em apenas UM namespace
        # print(str(slices_iterator))

        # adapter_port = adapter_dict[slice_id][str(slices_iterator['name'])]['adapter_ssh_port']
        adapter_port = adapter_dict[slice_id][str(slices_iterator['dc-slice-part']['name'])]['adapter_ssh_port']

        for service_it in slices_iterator['dc-slice-part']['vdus']:
            # print("service it ==== " + str(service_it))
            resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/createService", data = json.dumps(service_it['vdu']['commands']))
            #resp = requests.post("http://0.0.0.0:" + "1010" + "/createService", data = json.dumps(service_it['commands']))
            # print(str(service_it['commands']))
            # parsed_resp = resp.content.decode('utf-8')
            # services_status.append(parsed_resp)
        time.sleep(30)
            
    # return "Commands outputs = " + ('\n'.join(services_status))
    return 'OK'

@app.route('/deleteService', methods = ['POST']) 
def delete_service():
    # carrega o body do POST e "parseia" pra Json  
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)
    services_status = []

    for service_it in json_content['slice_parts']:
        # pra cada slice_part do yaml vai adicionar N servicos, mas em apenas UM namespace
        adapter_port = adapter_dict[json_content['slice_id']][service_it['slice_part_id']]['port']
        resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/deleteService", data = json.dumps(service_it))
        parsed_resp = resp.content.decode('utf-8')
        services_status.append(parsed_resp)
    return ('\n'.join(services_status))

@app.route('/updateService', methods = ['POST']) 
def update_service():
    # carrega o body do POST e "parseia" pra Json  
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    adapter_port = adapter_dict[json_content['slice_id']][json_content['slice_part_id']]['port']
    adapter_port = adapter_dict[json_content['slice_id']][json_content['slice_part_id']]['ssh_port']

    adapter_dict[slice_id][str(slices_iterator['dc-slice-part']['name'])]['adapter_ssh_port']

    if json_content['flag'] == "replica":
        resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/replicaScale", data = json.dumps(json_content['slices']['sliced'][slice_id]['slice-parts']['vdus']['commands']))
    elif json_content['flag'] == "redeploy":  
        requests.post("http://0.0.0.0:" + str(adapter_ssh_port) + "/deleteService", data = json.dumps(json_content['slices']['sliced'][slice_id]['slice-parts']))
        resp = requests.post("http://0.0.0.0:" + str(adapter_ssh_port) + "/createService", data = json.dumps(json_content['slices']['sliced'][slice_id]['slice-parts']['vdus']['commands']))
    else: 
        return 'Error: The yaml sent has a invalid flag.'
    return 'OK'

    resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/updateService", data = str(json_content))
    return str(resp.status_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')

#TODO
#- perguntar sobre retorno (a resposta eu que configuro? tem como voltar tanto uma resposta como um numero)
#- fazer arquivo global_dict ficar invisivel ao usuario (e read only???) [CONTRA: se fizer isso e deletar o adapter no portainer, programa morre]

#TESTS
#- verificar se podemos escolher pra qual worker o serviço vai
