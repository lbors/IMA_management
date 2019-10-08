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

@app.route('/setInitialConfig', methods = ['POST'])
def set_IP():
    global master_ip, master_port
    post_data = request.data.decode('utf-8')
    post_data = post_data.split(':')
    master_ip = post_data[0]
    master_port = post_data[1]

    print("IP do master: " + master_ip + "\tPorta do master: " + master_port)
    client = docker.from_env()
    client.swarm.join(remote_addrs = [str(master_ip) + ':' + str(master_port)], join_token = post_data[2])
    return 'OK'

@app.route('/')
def default_options():
    return "Welcome to the Swarm's adapter of Resource and VM Management! This is in early stage."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')



#TODO 
#- melhorar leitura
#- deixar bonito???????
