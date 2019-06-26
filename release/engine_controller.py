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

        client = docker.from_env()
        client.containers.run("agentwill:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
        print("http://0.0.0.0:" + str(port) + "/setIPandPort")
        time.sleep(3)
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

        requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
        print("The Adapter", agent_name, "has started")

@app.route('/')
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

@app.route('/listAdapters', methods = ['GET'])
def list_adapters():
    print(json.dumps(adapter_dict, indent=2))
    return 'OK'
    
@app.route('/updateManagement', methods = ['POST'])
def update_management():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    if json_content['flag'] == "append":
        start_slice_adapter(json_content)
        save_dict()
    elif json_content['flag'] == "delete":  
        client = docker.from_env()
        container = client.containers.get(str(json_content['slice-part-id']))
        container.stop()
        container.remove()
        adapter_dict[json_content['slice-id']].pop(json_content['slice-part-id'])
        save_dict()
    else: 
        return 'Error: The yaml sent has a invalid flag.'
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
    save_dict()
    return '200'

@app.route('/stopManagement', methods = ['POST'])
def stop_management():
    post_data = request.data.decode('utf-8') # exemplo de entrada: "Telefonica"

    for slice_part_it in adapter_dict[post_data]:
        client = docker.from_env()
        container = client.containers.get(slice_part_it)
        container.stop()
        container.remove()
    adapter_dict.pop(post_data)
    print('The slice ' + post_data + ' has been deleted.')
    save_dict()
    return '200'
    # print('Adapter not found')
    # return '400'

# def stop_ma():
#     return 'Stopping the Resource and VM Management infrastructure'


# SERVICES ########################################################################

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

    for service_it in json_content['slice_parts']:
        # pra cada slice_part do yaml vai adicionar N servicos, mas em apenas UM namespace
        adapter_port = adapter_dict[json_content['slice_id']][service_it['slice_part_id']]['port']
        # print(json.dumps(service_it, indent=2))
        resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/createService", data = json.dumps(service_it))
        
    # parsed = json.loads(resp.content)
    # print(json.dumps(parsed, indent=2))
    return str(resp.content)
    # return 'Adapter not found'

@app.route('/deleteService', methods = ['POST']) 
def delete_service():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    adapter_port = adapter_dict[json_content['slice_id']][json_content['slice_part_id']]['port']
    resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/deleteService", data = json.dumps(json_content))
    return 'OK'
    # return 'Adapter not found'

@app.route('/updateService', methods = ['POST']) 
def update_service():
    # ler arquivo de parametro
    file_name = request.data.decode('utf-8')
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    # carrega o YAML e "parseia" pra Json  
    data = yaml.safe_load(yaml_content)
    json_content = json.dumps(data)
    json_content = json.loads(json_content)

    adapter_port = adapter_dict[json_content['slice_id']][json_content['slice_part_id']]['port']

    if json_content['flag'] == "replica":
        update = "replica"
    elif json_content['flag'] == "delete":  
        update = "delete"
    else: 
        return 'Error: The yaml sent has a invalid flag.'
    return 'OK'

    resp = requests.post("http://0.0.0.0:" + str(adapter_port) + "/updateService", data = str(json_content))
    return str(resp.status_code)
    # return 'Adapter not found'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')


#PERGUNTAR
#- stopSlicePart precisa existir?

#TODO
#- perguntar sobre retorno (a resposta eu que configuro? tem como voltar tanto uma resposta como um numero)
#- fazer arquivo global_dict ficar invisivel ao usuario (e read only???) [CONTRA: se fizer isso e deletar o adapter no portainer, programa morre]
#- mudar chamadas de file-name pra file-content
#- avançar update

#TESTS
#- verificar se podemos escolher pra qual worker o serviço vai
#- testar /createService em dois VIMs (2 workers, 2 masters diferentes)