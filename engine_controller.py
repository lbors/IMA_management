from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
from subprocess import call

app = Flask(__name__)
slice_dict = {"slice":[]}
port_server = 8080
port = 5001
master_ip = '192.168.1.151'

def start_slice_adapter(json_content):
    global slice_dict
    global port
    
    #Start container for the IMA Agents/Adapters
    for i in json_content['dc-slice-part']:
        slice_name = i['name']
        slice_user = i['user']
        agent_name = slice_name + '_' + slice_user + '_agent'
        # print ('Nome da slice:' + str(slice_name))

        for j in i['vdus']: #???????????
            if str(j['dc-vdu']['type']) == "master":
                temp_ip = str(j['dc-vdu']['ip-address'])

        client = docker.from_env()
        client.containers.run("agentima:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})

        # requests.post("http://0.0.0.0:" + str(port) + "/setIP", data = temp_ip)
        print("The Adapter", agent_name, "has started")
        port = port + 1 

@app.route('/')address
def default_options():
    return 'Welcome to Resource and VM Management of IMA!'

# @app.route('/startManagementAdapter', methods = ['POST'])
# def start_monitoring():
#     params = request.data.decode('utf-8')
#     print("Imprimindo os params" + params)
#     # command = "python3.6 IMAv2/slice_aggregator/slice_aggregator.py " + params + " & >> agg_main.log"
#     command = "python3.6 IMA_management/engine_controller/engine_controller.py"
#     call(command, shell=True)

#     return "Starting Monitoring infrastructure"


@app.route('/startManagementAdapter', methods = ['POST'])
def start_monitoring():
    #print(request.headers)
    file_name = request.data.decode('utf-8')
    print(file_name)
    file = open(file_name, "r")
    yaml_content = file.read()
    file.close()

    json_content = json.dumps(yaml.safe_load(yaml_content))
    json_content = json.loads(json_content)
    # slice_id = json_content['slice']['id']

    # start_slice_aggregator(slice_id)
    start_slice_adapter(json_content)
    return 'OK'

@app.route('/stopManagementAdapter')
def stop_monitoring():
    return 'Stopping the Resource and VM Management infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')




#possiveis erros:
#- maquina ta subindo com ip que nao é 0.0.0.0