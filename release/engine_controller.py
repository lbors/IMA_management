from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
import socket
import time
import threading
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

@app.route('/')
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

@app.route('/listAdapters', methods = ['GET'])
def list_adapters():
    # print(json.dumps(adapter_dict, indent=2))
    return str(json.dumps(adapter_dict, indent=2))

def create_adapter(slice_id, slice_part_id, port, json_content):
    global adapter_dict

    master_ip = "null"
    for j in range(len(json_content['dc-slice-part']['VIM']['vdus'])): 
        if str(json_content['dc-slice-part']['VIM']['vdus'][j]['vdu']['type']) == "master": 
            master_ip = str(json_content['dc-slice-part']['VIM']['vdus'][j]['vdu']['ip'])

    if json_content['dc-slice-part']['VIM']['name'] == "SSH":
        agent_name = slice_part_id + '_adapter_ssh'
        ssh_ip = json_content['dc-slice-part']['VIM']['vim-ref']['ip-ssh']
        ssh_port = json_content['dc-slice-part']['VIM']['vim-ref']['port-ssh']
        ssh_user = json_content['dc-slice-part']['VIM']['vim-credential']['user-ssh']
        ssh_pass = json_content['dc-slice-part']['VIM']['vim-credential']['password-ssh']
        client = docker.from_env()
        client.containers.run("adapter_ssh:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        master_data = ssh_ip + ":" + str(ssh_port) + ":" + ssh_user + ":" + ssh_pass + ":" + str(port) + ":" + master_ip

        while True:
            try:
                requests.post("http://0.0.0.0:" + str(port) + "/setSSH", data = master_data)
                break
            except requests.exceptions.ConnectionError:
                pass
        print("The Adapter", agent_name, "has started")

        if slice_id in adapter_dict:
                adapter_dict[slice_id].update({ 
                        slice_part_id: ({
                            "port":str(port),
                            "adapter_ssh_name": agent_name,
                            "type": "SSH",
                            'ssh_ip': str(ssh_ip),
                            'ssh_port': str(ssh_port),
                            # 'ssh_user': str(ssh_user),
                            # 'ssh_pass': str(ssh_pass),
                            # 'master_ip': str(master_ip)
                        })
                })
        else:
            adapter_dict.update({
                slice_id: {
                    slice_part_id: ({
                        'port': str(port),
                        'adapter_ssh_name': agent_name,
                        "type": "SSH",
                        'ssh_ip': str(ssh_ip),
                        'ssh_port': str(ssh_port),
                        # 'ssh_user': str(ssh_user),
                        # 'ssh_pass': str(ssh_pass),
                        # 'master_ip': str(master_ip)
                        })
                    }
                })
    elif json_content['dc-slice-part']['VIM']['name'] == "KUBERNETES":
        agent_name = slice_part_id + '_adapter_k8s'
        client = docker.from_env()
        client.containers.run("adapter_k8s:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        temp_ip = str(json_content['dc-slice-part']['VIM']['vim-ref']['ip-api'])
        temp_port = str(json_content['dc-slice-part']['VIM']['vim-ref']['port-api'])
        master_data = temp_ip + ":" + str(temp_port)

        while True:
            try:
                requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
                break
            except requests.exceptions.ConnectionError:
                pass

        print("The Adapter", agent_name, "has started")

        if slice_id in adapter_dict:
                adapter_dict[slice_id].update({ 
                        slice_part_id: ({
                            "adapter_api_name":agent_name, 
                            "type": "KUBERNETES",
                            "port": str(port),
                            "api-ip": temp_ip,
                            "api-port": temp_port
                        })
                })
        else:
            adapter_dict.update({
                slice_id: {
                    slice_part_id: ({
                        "adapter_api_name":agent_name, 
                        "type": "KUBERNETES",
                        "port":str(port),
                        "api-ip": temp_ip,
                        "api-port": temp_port
                        })
                    }
                })

    elif json_content['dc-slice-part']['VIM']['name'] == "SWARM":
        agent_name = slice_part_id + '_adapter_swm'
        client = docker.from_env()
        client.containers.run("adapter_swm:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        temp_ip = str(json_content['dc-slice-part']['VIM']['vim-ref']['ip-api'])
        temp_port = str(json_content['dc-slice-part']['VIM']['vim-ref']['port-api'])
        initial_config = temp_ip + ":" + str(temp_port)

        while True:
            try:
                requests.post("http://0.0.0.0:" + str(port) + "/setInitialConfig", data = initial_config)
                break
            except requests.exceptions.ConnectionError:
                pass

        print("The Adapter", agent_name, "has started")

        if slice_id in adapter_dict:
                adapter_dict[slice_id].update({ 
                        slice_part_id: ({
                            "adapter_api_name":agent_name, 
                            "type": "SWARM",
                            "port":str(port),
                            "api-ip": temp_ip,
                            "api-port": temp_port
                        })
                })
        else:
            adapter_dict.update({
                slice_id: {
                    slice_part_id: ({
                        "adapter_api_name":agent_name, 
                        "type": "SWARM",
                        "port":str(port)
                        "api-ip": temp_ip,
                        "api-port": temp_port
                        })
                    }
                })
    else:
        print("Invalid VIM name. Must be 'KUBERNETES', 'SWARM' or 'SSH'.")

def start_slice_adapterv2(json_content):
    global adapter_dict
    threads = []
    slice_id = json_content['slice']['id']
    adapter_dict.update({slice_id:{}})

    for i in range(len(json_content['slice']['slice-parts'])):
        slice_part_id = json_content['slice']['slice-parts'][i]['dc-slice-part']['name']

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
        s.close()

        t = threading.Thread(target=create_adapter,args=(slice_id, slice_part_id, port, json_content['slice']['slice-parts'][i],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    save_dict()
    return "The Adapters was started!"

def delete_container(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    try:
        container.stop()
    except:
        pass
    try:
        container.remove()
    except:
        pass

@app.route('/necos/ima/update_management', methods = ['POST'])
def update_management():
    global adapter_dict
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data) 
    json_content = json.loads(json_content)

    if json_content['slice']['id'] in adapter_dict:
        i = 0
        for i in range(len(json_content['slice']['slice-parts'])):
            slice_part_id = json_content['slice']['slice-parts'][i]['dc-slice-part']['name']
            if slice_part_id in adapter_dict[json_content['slice']['id']]:
                print("Deleting adapter '" + slice_part_id + "_adapter_ssh" + "'")
                delete_container(slice_part_id+"_adapter_ssh")
                print("The Adapter '" + slice_part_id + "_adapter_ssh" + "' has been deleted.")
                adapter_dict[json_content['slice']['id']].pop(slice_part_id)
            else:
                print("Creating adapter '" + slice_part_id + "_adapter_ssh" + "'")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('localhost', 0))
                port = s.getsockname()[1]
                s.close()
                create_adapter(json_content['slice']['id'], slice_part_id, port, json_content['slice']['slice-parts'][i])
        save_dict()
        return str(json.dumps(adapter_dict, indent=2))
    else:
        return "Error: The slice ID in the yaml doesn't exists."

@app.route('/necos/ima/start_management', methods = ['POST'])
def start_management():
    json_content = json.dumps(yaml.safe_load(request.data.decode('utf-8')))
    json_content = json.loads(json_content)
    start_slice_adapterv2(json_content)
    save_dict()

    return str(json.dumps(adapter_dict, indent=2))

@app.route('/necos/ima/stop_management', methods = ['POST'])
def stop_management():
    global adapter_dict
    post_data = request.data.decode('utf-8') # exemplo de entrada: "Telefonica"
    threads = []    

    for slice_part in adapter_dict[post_data]:
        if "adapter_ssh_name" in adapter_dict[post_data][slice_part]:
            t = threading.Thread(target=delete_container,args=(adapter_dict[post_data][slice_part]["adapter_ssh_name"],))
            threads.append(t)
            t.start()
        elif "adapter_api_name" in adapter_dict[post_data][slice_part]: 
            t = threading.Thread(target=delete_container,args=(adapter_dict[post_data][slice_part]["adapter_api_name"],))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    adapter_dict.pop(post_data)
    save_dict()
    return str('The slice ' + post_data + ' has been deleted.')

# SERVICES ########################################################################
@app.route('/necos/ima/deploy_service', methods = ['POST']) 
def deploy_service():
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    slice_id = json_content['slices']['sliced']['id']
    for slices_iterator in json_content['slices']['sliced']['slice-parts']:
        adapter_port = adapter_dict[slice_id][str(slices_iterator['name'])]['port']

        for service_it in slices_iterator['vdus']:
            if service_it['VIM'] == "SSH":
                print("Executing the commands: ")
                print(str(json.dumps(service_it['commands'], indent=2)))
                requests.post("http://0.0.0.0:" + str(adapter_port) + "/deployService", data = json.dumps(service_it['commands']))
            elif service_it['VIM'] == "KUBERNETES":
                # adapter_port = adapter_dict[json_content['slice_id']][service_it['slice_part_id']]['port']
                print("Creating a K8s service...")
                resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/deployService", data = json.dumps(service_it))
                print(json.dumps(resp.json(), indent=2))
            elif service_it['VIM'] == "SWARM":
                print("Creating docker swarm service: " + str(service_it['service_info']['Name']))
                resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/deployService", data = json.dumps(service_it))
                print(json.dumps(resp.json(), indent=2))
                # se criar duas vezes ele faz um update
            else:
                print("Invalid VIM name. Must be 'KUBERNETES', 'SWARM' or 'SSH'.")

    # if slice_id == 'IoTService_sliced':
    #     time.sleep(30)       # MUDAR PRA 30 NO FIM DA IMPLEMENTACAO (?)
    return 'The Service for ' + slice_id + ' was created!'

@app.route('/necos/ima/delete_service', methods = ['POST']) 
def delete_service():
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    slice_id = json_content['slices']['sliced']['id']
    count = 0
    for slices_iterator in json_content['slices']['sliced']['slice-parts']:
        adapter_port = adapter_dict[slice_id][str(slices_iterator['name'])]['port']
        adapter_type = adapter_dict[slice_id][str(slices_iterator['name'])]['type']

        if adapter_type == "KUBERNETES":
            print("Deleting the services:")
            for service_it in slices_iterator['vdus']:
                print(" " + str(service_it['service_info']['metadata']['name']))
                resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/deleteService", data = json.dumps(service_it))
                # print(resp)
                count += 1
        else:   # swarm
            print("Deleting the services: " + str(slices_iterator['service-id']))
            resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/deleteService", data = json.dumps(slices_iterator))
            print(json.dumps(resp.json(), indent=2))
            count += 1
            
    # if slice_id == 'IoTService_sliced':
    #     time.sleep(30)      
    return (str(count) + ' services on the ' + slice_id + ' were deleted')

@app.route('/necos/ima/list_service', methods = ['POST']) 
def get_service():
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    slice_id = json_content['slices']['sliced']['id']

    for slices_iterator in json_content['slices']['sliced']['slice-parts']:
        adapter_port = adapter_dict[slice_id][str(slices_iterator['name'])]['port']
        adapter_type = adapter_dict[slice_id][str(slices_iterator['name'])]['type']

        if adapter_type == "SSH":
            return 'Could not list the services'
        elif adapter_type == "KUBERNETES":
            resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/listServices", data = json.dumps(slices_iterator))
            print(json.dumps(resp.json(), indent=2))
        elif adapter_type == "SWARM":
            resp = requests.get("http://0.0.0.0:" + str(adapter_port) + "/listServices")
            print(json.dumps(resp.json(), indent=2))
        else:
            print("Invalid VIM name. Must be 'KUBERNETES', 'SWARM' or 'SSH'.")

    # if slice_id == 'IoTService_sliced':
    #     time.sleep(30)       # MUDAR PRA 30 NO FIM DA IMPLEMENTACAO (?)
    
    return json.dumps(resp.json(), indent=2)


# FUNCAO INCOMPLETA, FALTA REVISAO
@app.route('/necos/ima/update_service', methods = ['POST']) 
def update_service():
    # carrega o body do POST e "parseia" pra Json  
    data = yaml.safe_load(request.data.decode('utf-8'))
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    slice_id = json_content["slices"]["sliced"]["id"]
    count = 0
    for slices_iterator in json_content['slices']['sliced']['slice-parts']:
        
        adapter_port = adapter_dict[slice_id][str(slices_iterator['name'])]['port']
        adapter_type = adapter_dict[slice_id][str(slices_iterator['name'])]['type']

        if adapter_type == "KUBERNETES":
            print("Updating the services:")
            for service_it in slices_iterator['vdus']:
                print(" " + str(service_it['service_info']['metadata']['name']))
                resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/updateService", data = json.dumps(service_it))
                print(json.dumps(resp.json(), indent=2))
        else:   # swarm
            for service_it in slices_iterator['vdus']:
                print("Updating the services: " + str(service_it['service_info']['Name']))
                resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/updateService", data = json.dumps(service_it))
                print(json.dumps(resp.json(), indent=2))

    return json.dumps(resp.json(), indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
