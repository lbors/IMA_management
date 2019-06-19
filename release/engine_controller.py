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

    for adapter_iterator in adapter_dict['adapters']:
      if adapter_iterator['slice_id'] == json_content['slice_id']:
          for slice_part_it in adapter_iterator['parts']:
              if slice_part_it['slice_part_id'] == json_content['slice_part_id']:
                  resp = requests.post("http://0.0.0.0:" + slice_part_it['port'] + "/deleteService", data = json.dumps(json_content))
                  return 'OK'
    return 'Adapter not found'

def save_dict():
    #filename = ""
    write_file = open("global_dict.json", 'w')
    json.dump(adapter_dict, write_file)
    write_file.close() 

def load_dict_NEW():
    jstring = ''.join(open('global_dict.json', 'r').readlines())
    d = {i['slice_id']: {j['slice_part_id']: ({'adapter_name': j['adapter_name'], 'port': j['port']}) for j in i['parts']} for i in json.loads(jstring)['adapters']}
    return d

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

    for adapter_iterator in adapter_dict['adapters']:
      if adapter_iterator['slice_id'] == json_content['slice_id']:
          for slice_part_it in adapter_iterator['parts']:
              if slice_part_it['slice_part_id'] == json_content['slice_part_id']:
                  resp = requests.post("http://0.0.0.0:" + slice_part_it['port'] + "/createService", data = str(json_content))
                  # parsed = json.loads(resp.content)
                  # print(json.dumps(parsed, indent=2))
                  return str(resp.status_code)
    return 'Adapter not found'

def start_slice_adapter(json_content):
    global adapter_dict
    
    #Start container for the IMA Agents/Adapters
    adapter_dict["adapters"].append({"slice_id":json_content['slice-id'],"parts":[]})
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
        for k in adapter_dict['adapters']:
            if k['slice_id'] == json_content['slice-id']:
                k['parts'].append({"slice_part_id":slice_name,"adapter_name":agent_name,"port":str(port)})
        # adapter_dict["adapters"].append({"slice_part_id":slice_name,"adapter_name":agent_name,"port":str(port)})

        requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
        print("The Adapter", agent_name, "has started")


@app.route('/')
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

@app.route('/listAdapters', methods = ['GET'])
def list_adapters():
    print(json.dumps(adapter_dict, indent=2))
    return 'OK'
    
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
    save_dict()
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


# def stop_ma():
#     return 'Stopping the Resource and VM Management infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')




#TODO
#- perguntar sobre retorno (a resposta eu que configuro? tem como voltar tanto uma resposta como um numero)
#- fazer arquivo global_dict ficar invisivel ao usuario (e read only???) [CONTRA: se fizer isso e deletar o adapter manualmente, programa morre]
#- mudar chamadas de file-name pra file-content
#- funcao "reset" (apagar dict)

#TESTS
#- verificar se podemos escolher pra qual worker o serviço vai
#- testar /createService em dois VIMs (2 workers, 2 masters diferentes)
#- começar update (orientado á tecnologia)

""" jstring = ''.join(open('example_dict.json', 'r').readlines())
aqui vc le o json como string
d = {i['slice_id']: {j['slice_part_id']: (j['adapter_name'], j['port']) for j in i['parts']} for i in json.loads(jstring)['adapters']}
aqui vc le e constrói como um dict

aí é só acessar assim: d['Claro']['slice-02']
eu não sei o que vai ser chave na sua busca, mas aí é só mudar no código (posso explicar melhor como, se vc quiser) """