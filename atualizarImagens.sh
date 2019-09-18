#!/bin/bash
sudo docker build -f Dockerfiles/Dockerfile_ssh -t adapter_ssh . --no-cache
sudo docker build -f Dockerfiles/Dockerfile_k8s -t adapter_k8s . --no-cache
sudo docker build -f Dockerfiles/Dockerfile_swm -t adapter_swm . --no-cache
echo 'Fim!'