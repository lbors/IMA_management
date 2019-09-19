#Start Dojot Slice

curl -X POST http://localhost:5001/necos/ima/start_management --header "Content-type:application/yaml" \
-d 'slice:
  id: IoTService_sliced
  slice-parts:
  - dc-slice-part:
      VIM:
        name: SSH
        vdus:
        - vdu:
            description: Master (controller) of kubernetes cluster
            id: k8s-master_5
            ip: 10.10.5.1
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of kubernetes cluster
            id: k8s-node_5
            ip: 10.10.5.2
            name: k8s-node
            type: worker
            vdu-image: k8s-dojot-min-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 10.1.0.3
          ip-ssh: 10.1.0.3
          port-api: 21100
          port-ssh: 22100
      name: dc-slice2
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Compute node of SSH cluster
            id: k8s-node2_2
            ip: 10.10.2.3
            name: k8s-node2
            type: worker
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of SSH cluster
            id: k8s-node1_2
            ip: 10.10.2.2
            name: k8s-node1
            type: worker
            vdu-image: k8s-dojot-template
        - vdu:
            description: Master (controller) of SSH cluster
            id: k8s-master_2
            ip: 200.18.102.28
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 200.18.102.28
          ip-ssh: 143.106.11.131
          port-api: 8080
          port-ssh: 22143
      name: dc-slice1'
 

 # Stop Dojot Slice
curl -X POST http://localhost:5001/necos/ima/stop_management -d 'IoTService_sliced' --header "Content-Type:application/yaml"


 # Start Touristic Slice
 curl -X POST http://localhost:5001/necos/ima/start_management --header "Content-type:application/yaml" \
-d 'slice:
  id: TouristicCDN_sliced
  slice-parts:
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Compute node for CDN deployment
            id: k8s-node_4
            ip: 10.10.4.2
            name: k8s-node
            type: worker
            vdu-image: k8s-cdn-template
        - vdu:
            description: Master node for CDN deployment
            id: k8s-master_4
            ip: 10.10.4.1
            name: k8s-master
            type: master
            vdu-image: k8s-cdn-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 200.133.239.38
          ip-ssh: 200.133.239.38
          port-api: 21008
          port-ssh: 22008
      name: edge-dc-slice-brazil
  - dc-slice-part:
      VIM:
        name: xen-vim
        vdus:
        - vdu:
            description: load balancer and content services
            id: core_vm_2
            ip: 10.10.2.1
            name: core_vm
            type: 'null'
            vdu-image: core-vm-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 'null'
          ip-ssh: 143.106.11.131
          port-api: 'null'
          port-ssh: 22131
      name: core-dc
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Compute node for CDN deployment
            id: k8s-node_5
            ip: 10.10.5.2
            name: k8s-node
            type: worker
            vdu-image: k8s-cdn-template
        - vdu:
            description: Master node for CDN deployment
            id: k8s-master_5
            ip: 10.10.5.1
            name: k8s-master
            type: master
            vdu-image: k8s-cdn-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 10.1.0.3
          ip-ssh: 10.1.0.3
          port-api: 21092
          port-ssh: 22092
      name: edge-dc-slice-spain
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Compute node for CDN deployment
            id: k8s-node_6
            ip: 10.10.6.2
            name: k8s-node
            type: worker
            vdu-image: k8s-cdn-template
        - vdu:
            description: Master node for CDN deployment
            id: k8s-master_6
            ip: 10.10.6.1
            name: k8s-master
            type: master
            vdu-image: k8s-cdn-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 195.251.209.100
          ip-ssh: 195.251.209.100
          port-api: 21031
          port-ssh: 22031
      name: edge-dc-slice-greece'

 # Stop Touristic Slice
 curl -X POST http://localhost:5001/necos/ima/stop_management -d 'TouristicCDN_sliced' --header "Content-Type:application/yaml"

 # Update Dojot Slice

curl -X POST http://localhost:5001/necos/ima/start_management --header "Content-type:application/yaml" \
-d 'slice:
  id: IoTService_sliced
  slice-parts:
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Master (controller) of kubernetes cluster
            id: k8s-master_5
            ip: 10.10.5.1
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of kubernetes cluster
            id: k8s-node_5
            ip: 10.10.5.2
            name: k8s-node
            type: worker
            vdu-image: k8s-dojot-min-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 10.1.0.3
          ip-ssh: 10.1.0.3
          port-api: 21100
          port-ssh: 22100
      name: dc-slice2'

curl -X POST http://localhost:5001/necos/ima/update_management --header "Content-type:application/yaml" \
-d 'slice:
  id: IoTService_sliced
  slice-parts:
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Compute node of kubernetes cluster
            id: k8s-node2_2
            ip: 10.10.2.3
            name: k8s-node2
            type: worker
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of kubernetes cluster
            id: k8s-node1_2
            ip: 10.10.2.2
            name: k8s-node1
            type: worker
            vdu-image: k8s-dojot-template
        - vdu:
            description: Master (controller) of kubernetes cluster
            id: k8s-master_2
            ip: 10.10.2.1
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 143.106.11.131
          ip-ssh: 143.106.11.131
          port-api: 21143
          port-ssh: 22143
      name: dc-slice1'  

# Deploy Service Test 

curl -X POST http://localhost:5001/necos/ima/start_management --header "Content-type:application/yaml" \
-d 'slice:
  id: IoTService_sliced
  slice-parts:
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Master (controller) of kubernetes cluster
            id: k8s-master_5
            ip: 10.10.5.1
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of kubernetes cluster
            id: k8s-node_5
            ip: 10.10.5.2
            name: k8s-node
            type: worker
            vdu-image: k8s-dojot-min-template
        vim-credential:
          password-ssh: openstack
          user-ssh: andre
        vim-ref:
          ip-api: 10.1.0.3
          ip-ssh: 192.168.15.3
          port-api: 21100
          port-ssh: 22
      name: dc-slice1'



curl -X POST http://localhost:5001/necos/ima/deploy_service --header "Content-type:application/text" \
-d '
slices:
  sliced:
    id: IoTService_sliced
    slice-parts:
      - dc-slice-part:
        name: dc-slice1
        vdus:
          - vdu:
            commands:
              - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
              - ls >> t.txt
            name: k8s-master_2
            namespace: dojot
            VIM: KUBERNETES'

curl -X POST http://localhost:5001/necos/ima/deploy_service --header "Content-type:application/text" \
-d '
slices:
  sliced:
    id: IoTService_sliced
    slice-parts:
    - dc-slice-part: null
      name: dc-slice1
      vdus:
      - vdu: null
        commands:
          - ls >> t.txt
        name: k8s-master_2
        namespace: dojot
        VIM: KUBERNETES
    - dc-slice-part: null
      name: dc-slice1
      vdus:
      - vdu: null
        commands:
          - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
          - ls >> t2.txt
        name: k8s-master_2
        namespace: dojot
        VIM: KUBERNETES'

curl -X GET http://localhost:5001/listAdapters

sudo docker build -f Dockerfilessh -t adapter_ssh . --no-cache


# SERVICE DEPLOY SSH AND K8S SIMULTANEOUSLY

curl -X POST http://localhost:5001/necos/ima/start_management --header "Content-type:application/yaml" \
-d 'slice:
  id: Dojot
  slice-parts:
  - dc-slice-part:
      VIM:
        name: SSH
        vdus:
        - vdu:
            description: Master (controller) of kubernetes cluster
            id: k8s-master_5
            ip: 10.10.5.1
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of kubernetes cluster
            id: k8s-node_5
            ip: 10.10.5.2
            name: k8s-node
            type: worker
            vdu-image: k8s-dojot-min-template
        vim-credential:
          password-ssh: F
          user-ssh: F
        vim-ref:
          ip-api: 10.1.0.3
          ip-ssh: 200.18.102.19
          port-api: 21100
          port-ssh: 22
      name: dc-slice2
  - dc-slice-part:
      VIM:
        name: KUBERNETES
        vdus:
        - vdu:
            description: Compute node of SSH cluster
            id: k8s-node2_2
            ip: 10.10.2.3
            name: k8s-node2
            type: worker
            vdu-image: k8s-dojot-template
        - vdu:
            description: Compute node of SSH cluster
            id: k8s-node1_2
            ip: 10.10.2.2
            name: k8s-node1
            type: worker
            vdu-image: k8s-dojot-template
        - vdu:
            description: Master (controller) of SSH cluster
            id: k8s-master_2
            ip: 200.18.102.28
            name: k8s-master
            type: master
            vdu-image: k8s-dojot-template
        vim-credential:
          password-ssh: necos
          user-ssh: root
        vim-ref:
          ip-api: 200.18.102.28
          ip-ssh: 143.106.11.131
          port-api: 8080
          port-ssh: 22143
      name: dc-slice1'

curl -X POST http://localhost:5001/necos/ima/deploy_service --header "Content-type:application/text" \
-d '
slices:
    sliced:
      id: Dojot
      slice-parts:
      - dc-slice-part: null
        name: dc-slice2
        vdus:
          - vdu:
            commands:
              - git clone https://github.com/LABORA-INF-UFG/NECOS-ansible-dojot-core.git
            name: k8s-master_2
            namespace: dojot
            VIM: SSH
      - dc-slice-part: null
        name: dc-slice1
        vdus:
          - vdu:
            name: k8s-master_2
            namespace: dojot
            VIM: KUBERNETES
            service_info:
              apiVersion: v1
              kind: Pod
              metadata:
                name: nginx
                labels:
                  name: nginx
              spec:
                containers:
                - name: nginx
                  image: nginx
                  ports:
                    - containerPort: 443
                  volumeMounts:
                    - mountPath: "/etc/nginx/"
                      name: "nginx-conf"
                    - mountPath: "/usr/local/etc/nginx/ssl"
                      name: "ssl-certs"
                volumes:
                  - name: "nginx-conf"
                    secret:
                      secretName: "nginx.conf"
                  - name: "ssl-certs"
                    secret:
              secretName: "nginx-ssl-certs"'
