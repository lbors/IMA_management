from flask import Flask, url_for, request
from flask_request_params import bind_request_params
import yaml
import requests
import docker
import json
from subprocess import call

app = Flask(__name__)

@app.route('/')
def default_options():
    return 'Welcome to Monitoring Engine Controller'

@app.route('/startMonitoring', methods = ['POST'])
def start_monitoring():
    params = request.data.decode('utf-8')
    print("Imprimindo os params" + params)
    command = "python3.6 IMAv2/agentIMA/agent_prometheusv2.py " + params + " & >> agent_prom.log"
    call(command, shell=True)

    return "Starting Monitoring Agent"

@app.route('/stopMonitoring/<stopMonitoring>')
def stop_monitoring():
    return 'Stoping the monitoring infrastructure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='1010')
