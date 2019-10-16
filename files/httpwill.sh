comandos uteis:
sudo docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
sudo docker build -t adapterk8s .  
sudo docker build -f Dockerfilessh -t adapter_ssh_k . --no-cache

# retorna uma string de boas vindas
curl --request GET http://0.0.0.0:5001/

# retorna o dict
curl --request GET http://0.0.0.0:5001/listAdapters

# inicia o management com uma VM
curl -X POST \
  http://0.0.0.0:5001/startManagement \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4c83cb0c-9407-476d-9b33-f86169521cc7' \
  -H 'cache-control: no-cache' \
  -d '---
slice-id: Telemarketing
dc-slice-part:
    -   slice-part:
        name: slice-part-test-01
        user: Telefonicas
        VIM: # VIM information
            VIM_Type_name: "Kubernetes"
        vdus: # Virtual Deployment Unit
            - dc-vdu: # data-center
                name: master-test-01
                ip-address: 200.18.102.80
                port: 8080
                description: load balancer for elastic CDN deployment 
                template_name: kube-template
                type: master
            - dc-vdu:
                name: worker-test-01
                ip-address: 10.10.10.71
                port: 8080
                description: load balancer for elastic CDN deployment 
                template_name: kube-template
                type: worker
            - dc-vdu:
                name: worker-test-02
                ip-address: 10.10.10.72
                port: 8080
                description: load balancer for elastic CDN deployment 
                template_name: kube-template
                type: worker'

# exclui uma slice do dict
curl --header "Content-Type: */yaml" --request POST --data 'Telefonica' http://0.0.0.0:5001/stopManagement

# faz um deploy do nginx na slice Telemarketing e na slice part = slice-part-test-01
curl -X POST \
  http://localhost:5001/deployService \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4e084f32-0677-4301-92d5-4262851d0d05' \
  -H 'cache-control: no-cache' \
  -d '---
slice_id: Telemarketing
slice_parts:
  - s:
    slice_part_id: slice-part-test-01
    namespace: default
    service_info:
      - service:  
        apiVersion: v1
        kind: Service
        metadata:
          name: nginx
          labels:
            app: nginx
        spec:
          selector:
            app: nginx
          ports:
          - port: 80
            name: http
            targetPort: 80
          - port: 443
            name: https
            targetPort: 80'

# deleta um servico "nginx" da slice Telemarketing (slice part = slice-part-test-01)
curl -X POST \
  http://localhost:5001/deleteService \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: b6c72f65-3efc-4c5a-a615-20b531930ff2' \
  -H 'cache-control: no-cache' \
  -d '---
slice_id: Telemarketing
slice_parts:
  - s:
    slice_part_id: slice-part-test-01
    namespace: default
    service_info:
      - service:  
        apiVersion: v1
        kind: Service
        metadata:
          name: nginx
          labels:
            app: nginx
        spec:
          selector:
            app: nginx
          ports:
          - port: 80
            name: http
            targetPort: 80
          - port: 443
            name: https
            targetPort: 80'

# deleta uma slice chamada Telemarketing (e todas as sliceIDs internas)
curl -X POST \
  http://localhost:5001/stopManagement \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: b6c72f65-3efc-4c5a-a615-20b531930ff2' \
  -H 'cache-control: no-cache' \
  -d 'Telemarketing'





# CURL para crir um cluster local
curl -X POST \
  http://0.0.0.0:5001/startManagement \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4c83cb0c-9407-476d-9b33-f86169521cc7' \
  -H 'cache-control: no-cache' \
  -d '---
slice-id: Telemarketing
dc-slice-part:
    -   slice-part:
        name: slice-part-01
        user: Telefonica1
        VIM: # VIM information
            VIM_Type_name: "Kubernetes"
            VIM_Type_access: "SSH"
            IP: "127.0.0.1"
            port: "22"
            user: "user"
            password: "senha"

        vdus: # Virtual Deployment Unit
            - dc-vdu: # data-center
                name: master-01
                ip-address: localhost
                port: 22 
                description: master de um worker 
                template_name: kube-template
                type: master
            - dc-vdu:
                name: worker-01
                ip-address: 200.136.191.26
                port: 8080
                description: worker com nginx 
                template_name: kube-template
                type: worker
    -   slice-part:
        name: slice-part-02
        user: Telefonica2
        VIM: # VIM information
            VIM_Type_name: "Kubernetes"
            VIM_Type_access: "SSH"
            IP: "Slice Part Entrypoint IP"
            port: "Slice Part SSH Port or API Port"
            user: "SSH user"
            password: "SSH password"

        vdus: # Virtual Deployment Unit
            - dc-vdu: # data-center
                name: master-02
                ip-address: 200.136.191.89
                port: 8080
                description: master de um worker 
                template_name: kube-template
                type: master
            - dc-vdu:
                name: worker-02
                ip-address: 200.136.191.108
                port: 8080
                description: worker com nginx 2
                template_name: kube-template
                type: worker'

# CURL para rodar comandos de teste
curl -X POST \
  http://localhost:5001/deployService \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4e084f32-0677-4301-92d5-4262851d0d05' \
  -H 'cache-control: no-cache' \
  -d '---
slices:
   sliced:
      id: IoTService_sliced
      slice-parts:     
         - dc-slice-part:
           name: dc-slice1
           vdus:
             - vdu:
               name: master-01
               VIM: Kubernetes
               commands: 
                - echo "Alo Mundo 1!"
                - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
                - ls
                - ls
                - echo "Alo Mundo 5!"
         - dc-slice-part:
           name: dc-slice2
           vdus:
             - vdu:
               name: master-02
               VIM: Kubernetes
               commands: 
                - echo "Alo Mundo 1!"
                - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
                - ls
                - ls
                - echo "Alo Mundo 5!"


# inicia o management v2
curl -X POST \
  http://0.0.0.0:5001/startManagement \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4c83cb0c-9407-476d-9b33-f86169521cc7' \
  -H 'cache-control: no-cache' \
  -d '---
slice-id: Telemarketing
dc-slice-part:
    -   slice-part:
        name: slice-part-01
        user: Telefonica1
        VIM: # VIM information
            VIM_Type_name: "Kubernetes"
            VIM_Type_access: "SSH"
            IP: 200.18.102.60
            port: 22
            user: debeltrami
            password: openstack

        vdus: # Virtual Deployment Unit
            - dc-vdu: # data-center
                name: master-01
                ip-address: 200.136.191.32
                port: 8080 
                description: master de um worker 
                template_name: kube-template
                type: master
            - dc-vdu:
                name: worker-01
                ip-address: 200.136.191.26
                port: 8080
                description: worker com nginx 
                template_name: kube-template
                type: worker
    -   slice-part:
        name: slice-part-02
        user: Telefonica2
        VIM: # VIM information
            VIM_Type_name: "Kubernetes"
            VIM_Type_access: "SSH"
            IP: 200.18.102.60
            port: 22
            user: debeltrami
            password: openstack

        vdus: # Virtual Deployment Unit
            - dc-vdu: # data-center
                name: master-02
                ip-address: 200.136.191.89
                port: 8080
                description: master de um worker 
                template_name: kube-template
                type: master
            - dc-vdu:
                name: worker-02
                ip-address: 200.136.191.108
                port: 8080
                description: worker com nginx 2
                template_name: kube-template
                type: worker'


curl -X POST http://localhost:1010/createService -d b'["echo \\"Alo Mundo 1!\\"", "echo \\"Alo Mundo 2!\\"", "echo \\"Alo Mundo 3!\\"", "echo \\"Alo Mundo 4!\\"", "echo \\"Alo Mundo 5!\\""]'

b'["echo \\"Alo Mundo 1!\\"", "echo \\"Alo Mundo 2!\\"", "echo \\"Alo Mundo 3!\\"", "echo \\"Alo Mundo 4!\\"", "echo \\"Alo Mundo 5!\\""]'

curl -X POST \
  http://localhost:5001/deployService \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4e084f32-0677-4301-92d5-4262851d0d05' \
  -H 'cache-control: no-cache' \
  -d '---
slices:
   sliced:
      id: Telemarketing
      slice-parts:     
         - dc-slice-part:
           name: slice-part-01
           vdus:
             - vdu:
               name: master-01
               VIM: Kubernetes
               commands: 
                - echo "Alo Mundo 1!"
                - sed -i "s/REPLACE/$coreip/" NECOS-ansible-dojot-core/inventories/example_local/group_vars/dojot-k8s/dojot.yaml
                - echo "Alo Mundo 5!"'



#Used by Deploy server test
curl -X POST \
  http://0.0.0.0:5001/necos/ima/start_management \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4c83cb0c-9407-476d-9b33-f86169521cc7' \
  -H 'cache-control: no-cache' \
  -d 'slice:
   id: IoTService_sliced
   slice-parts:
      - dc-slice-part:
         name: dc-slice1
         # user is not available
         VIM:
            name: KUBERNETES
            # VIM_Type_access is not available
            vim-ref:
               ip-api: 143.106.11.131
               ip-ssh: 143.106.11.131
               port-api: 21277
               port-ssh: 22277
            vim-credential: 
               user-ssh: "root"
               password-ssh: "necos"
            vdus:
               - vdu:
                  id: k8s-master
                  name: k8s-master
                  ip: 10.10.2.1
                  # port is not available
                  description: Master (controller) of kubernetes cluster
                  vdu-image: kube-template
                  type: master
               - vdu:
                  id: k8s-node
                  name: k8s-node1
                  ip: 10.10.2.2
                  # port is not available
                  description: Compute node of kubernetes cluster
                  vdu-image: kube-template
                  type: worker
               - vdu:
                  id: k8s-node
                  name: k8s-node2
                  ip: 10.10.2.3
                  # port is not available
                  description: Compute node of kubernetes cluster
                  vdu-image: kube-template
                  type: worker
               - vdu:
                  id: k8s-node
                  name: k8s-node3
                  ip: 10.10.2.4
                  # port is not available
                  description: Compute node of kubernetes cluster
                  vdu-image: kube-template
                  type: worker
      - dc-slice-part:
         name: dc-slice2
         # user is not available
         VIM:
            name: KUBERNETES
            # VIM_Type_access is not available
            vim-ref:
               ip-api: 10.1.0.3
               ip-ssh: 10.1.0.3
               port-api: 21564
               port-ssh: 22564
            vim-credential:
               user-ssh: "root"
               password-ssh: "necos"
            vdus:
               - vdu:
                  id: k8s-master
                  name: k8s-master
                  ip: 10.10.5.1
                  # port is not available
                  description: Master (controller) of kubernetes cluster
                  vdu-image: kube-template
                  type: master
               - vdu:
                  id: k8s-node
                  name: k8s-node
                  ip: 10.10.5.2
                  # port is not available
                  description: Compute node of kubernetes cluster
                  vdu-image: kube-template
                  type: worker'


# CURL para rodar o serviço
curl -X POST \
  http://localhost:5001/deployService \
  -H 'Content-Type: application/yaml' \
  -H 'Postman-Token: 4e084f32-0677-4301-92d5-4262851d0d05' \
  -H 'cache-control: no-cache' \
  -d '---
slices:
   sliced:
      id: IoTService_sliced
      slice-parts:     
         - dc-slice-part:
           name: dc-slice1
           vdus:
             - vdu:
               name: master-01
               VIM: Kubernetes
               commands: 
                  - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
                  - apt install -y python-pip
                  - pip install -r NECOS-ansible-dojot-core/requirements.txt
                  - sed -i "s/REPLACE/$coreip/" NECOS-ansible-dojot-core/inventories/example_local/group_vars/dojot-k8s/dojot.yaml
                  - ansible-playbook -K -k -i NECOS-ansible-dojot-core/inventories/example_local/ NECOS-ansible-dojot-core/deploy.yaml
         - dc-slice-part:
           name: dc-slice2
           vdus:
             - vdu:
               name: master-02
               VIM: Kubernetes
               commands: 
                  - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
                  - apt install -y python-pip
                  - pip install -r NECOS-ansible-dojot-core/requirements.txt
                  - sed -i "s/REPLACE/$coreip/" NECOS-ansible-dojot-core/inventories/example_local/group_vars/dojot-k8s/dojot.yaml
                  - ansible-playbook -K -k -i NECOS-ansible-dojot-core/inventories/example_local/ NECOS-ansible-dojot-core/deploy.yaml'