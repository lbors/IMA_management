def reset_dict():
    global adapter_dict
    adapter_dict = {}
    save_dict()

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
                # print(str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'][j]))
                if str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'][j]['vdu']['type']) == "master": # um campo type identifica o mestre 
                    master_ip = str(json_content['slice']['slice-parts'][i]['dc-slice-part']['VIM']['vdus'][j]['vdu']['ip']) 

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('localhost', 0))
            port = s.getsockname()[1]
            s.close()

            client = docker.from_env()
            client.containers.run("adapter_ssh:latest", detach=True, name=agent_name, ports={'1010/tcp': ('localhost', port)})
            
            while True:
                try:
                    requests.post("http://0.0.0.0:" + str(port) + "/setSSH", data = master_data)
                    break
                except requests.exceptions.ConnectionError:
                    pass

            if json_content['slice']['id'] in adapter_dict:
                adapter_dict[json_content['slice']['id']].update({ 
                        slice_name: ({
                            "port":str(port),
                            "adapter_ssh_name": agent_name,
                            'ssh_ip': str(ssh_ip),
                            'ssh_port': str(ssh_port),
                            'ssh_user': str(ssh_user),
                            'ssh_pass': str(ssh_pass),
                            'master_ip': str(master_ip)
                        })
                })
            else:
                adapter_dict.update({
                    json_content['slice']['id']: {
                        slice_name: ({
                            'port': str(port),
                            'adapter_ssh_name': agent_name,
                            'ssh_ip': str(ssh_ip),
                            'ssh_port': str(ssh_port),
                            'ssh_user': str(ssh_user),
                            'ssh_pass': str(ssh_pass),
                            'master_ip': str(master_ip)
                        })
                    }
                })
            
            master_data = ssh_ip + ":" + str(ssh_port) + ":" + ssh_user + ":" + ssh_pass + ":" + str(port) + ":" + master_ip
            # print("http://0.0.0.0:" + str(port) + "/setSSH")
            print("The Adapter", agent_name, "has started")
        else:
            if json_content['slice']['id'] in adapter_dict:
                adapter_dict[json_content['slice']['id']].update({ 
                        slice_name: ({
                            'adapter_ssh_name': 'null'
                        })
                })
            else:
                adapter_dict.update({
                    json_content['slice']['id']: {
                        slice_name: ({
                            'adapter_ssh_name': 'null'
                        })
                    }
                })

def create_container(slice_name, slice_part, adapter_type, json_content):
    # SSH OU API
    print(str(json.dumps(json_content, indent=2)))

    if adapter_type == "ssh":
        agent_name = slice_part + '_adapter_ssh'
        ssh_ip = json_content['dc-slice-part']['VIM']['vim-ref']['ip-ssh']
        ssh_port = json_content['dc-slice-part']['VIM']['vim-ref']['port-ssh']
        ssh_user = json_content['dc-slice-part']['VIM']['vim-credential']['user-ssh']
        ssh_pass = json_content['dc-slice-part']['VIM']['vim-credential']['password-ssh']
        # json_content['slice']['slice-parts'][i]

        master_ip = "null"

        for j in range(len(json_content['dc-slice-part']['VIM']['vdus'])): 
        # for para identificar o master sequencialmente
            # print(str(json_content['slice']['slice-parts'][i]['dc-slice-part']['dc-slice-part']['VIM']['vdus'][j]))
            if str(json_content['dc-slice-part']['VIM']['vdus'][j]['vdu']['type']) == "master": # um campo type identifica o mestre 
                master_ip = str(json_content['dc-slice-part']['VIM']['vdus'][j]['vdu']['ip']) 

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
        s.close()

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

        if slice_name in adapter_dict:
            adapter_dict[slice_name].update({ 
                    slice_part: ({
                        "port":str(port),
                        "adapter_ssh_name": agent_name,
                        'ssh_ip': str(ssh_ip),
                        'ssh_port': str(ssh_port),
                        'ssh_user': str(ssh_user),
                        'ssh_pass': str(ssh_pass),
                        'master_ip': str(master_ip)
                    })
            })
        else:
            adapter_dict.update({
                slice_name: {
                    slice_part: ({
                        'port': str(port),
                        'adapter_ssh_name': agent_name,
                        'ssh_ip': str(ssh_ip),
                        'ssh_port': str(ssh_port),
                        'ssh_user': str(ssh_user),
                        'ssh_pass': str(ssh_pass),
                        'master_ip': str(master_ip)
                    })
                }
            })

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
            
            while True:
                try:
                    requests.post("http://0.0.0.0:" + str(port) + "/setIPandPort", data = master_data)
                    break
                except requests.exceptions.ConnectionError:
                    pass

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
