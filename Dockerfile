FROM ubuntu:latest
RUN \
	apt update && \
	apt -y upgrade && \
    apt -y install python3-pip && \
    apt -y install iperf3 && \
    apt -y install iperf && \
    apt -y install stress && \
    apt -y install stress-ng && \
    apt -y install git && \
    apt -y install vim && \
    git clone https://github.com/williamgdo/IMA_management.git && \
    pip3 install requests && \
    pip3 install pika==0.13.1 && \
    pip3 install influxdb && \
    pip3 install flask && \
    pip3 install flask_request_params && \
    pip3 install pyyaml && \
    apt install net-tools && \
    pip3 install docker && \
    apt -y install iputils-ping && \
    cd IMA_management/ && \
    git checkout master && \
    git pull

ENTRYPOINT python3.6 IMA_management/adapter.py >> adapter.log