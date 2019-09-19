#!/bin/bash
echo '1/3 (Buildando adapter_ssh...)'
sudo docker build -f Dockerfiles/Dockerfile_ssh -t adapter_ssh . --no-cache
echo '2/3 (Buildando adapter_k8s...)'
sudo docker build -f Dockerfiles/Dockerfile_k8s -t adapter_k8s . --no-cache
echo '3/3 (Buildando adapter_swm...)'
sudo docker build -f Dockerfiles/Dockerfile_swm -t adapter_swm . --no-cache
echo 'Fim!'