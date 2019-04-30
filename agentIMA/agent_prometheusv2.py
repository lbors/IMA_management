# encoding: utf-8

import sys
import time
import requests
import json
from agent_producer import agent_producer
from datetime import timedelta, datetime


class agent_ima():

    def __init__(self, initial_config):
        initial_config = json.loads(initial_config)
        self.user = initial_config['queue_user']
        self.password = initial_config['queue_password']
        self.ip = initial_config['slice_provider_ip']
        self.port_queue = initial_config['queue_port']
        self.vhost = initial_config['vhost']
        self.slice_id = initial_config['slice_id']
        self.queue_name = initial_config['slice_id']
        self.slice_part_id = initial_config['slice_part_id']
        self.monitoring_tool = initial_config['monitoring_tool']
        self.monitoring_ip = initial_config['monitoring_ip']
        self.monitoring_port = initial_config['monitoring_port']
        self.interval = initial_config['monitoring_interval']
        self.metrics = initial_config['metrics']
   
    def get_metrics(self):
        if self.monitoring_tool == 'prometheus':
            URL = "http://%s:%s/api/v1/query?" % (self.monitoring_ip, self.monitoring_port)
            print(URL)
            metrics = []
            message = list()

            for i in range(len(self.metrics)):
                if self.metrics[i] == 'MEMORY_UTILIZATION_PHYSICAL':
                    # Métrica 1: Physical Memory used by node (%)
                    query = '((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_memory", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                    print("Metric Memory Node: %s\n" % metric)
                
                elif self.metrics[i] == 'CPU_UTILIZATION_PHYSICAL':
                    # Métrica 2: Physical CPU used by node (%)
                    query = '100 - (avg by (host) (irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_cpu", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                
                elif self.metrics[i] == 'TOTAL_BYTES_READS_PHYSICAL':
                    # Métrica 3: Bytes Reads Total (B)
                    query = 'sum(node_disk_reads_completed_total) by (host)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_bytes_reads", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                
                elif self.metrics[i] == 'TOTAL_BYTES_WRITES_PHYSICAL':
                    # Métrica 4: Bytes Writes Total (B)
                    query = 'sum(node_disk_writes_completed_total) by (host)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_bytes_writes", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                
                elif self.metrics[i] == 'TOTAL_BYTES_RX_PHYSICAL':
                    # Métrica 5: Bytes RX Total (B)
                    query = 'sum(node_network_receive_bytes_total) by (host)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_bytesRX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                
                elif self.metrics[i] == 'TOTAL_BYTES_TX_PHYSICAL':
                    # Métrica 6: Bytes TX Total (B)
                    query = 'sum(node_network_transmit_bytes_total) by (host)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_bytesTX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                
                elif self.metrics[i] == 'TOTAL_PACKETS_TX_PHYSICAL':
                    # Métrica 7: Packets TX Total (number)
                    query = 'sum(node_network_transmit_packets_total) by (host)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_packetsTX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

                elif self.metrics[i] == 'TOTAL_PACKETS_RX_PHYSICAL':
                    # Métrica 8: Packets RX Total (number)
                    query = 'sum(node_network_receive_packets_total) by (host)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['host']
                        resource_type = "Physical"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "node_packetsRX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
                
                elif self.metrics[i] == 'MEMORY_UTILIZATION_CONTAINER':
                    # Métrica 1: Container Memory used (B)
                    query = 'sum(container_memory_usage_bytes{name=~"[0-z]+"}) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_memory", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

                elif self.metrics[i] == 'CPU_UTILIZATION_CONTAINER':
                    # Métrica 2: Container CPU used (%)
                    query = 'sum(rate(container_cpu_usage_seconds_total{name=~"[0-z]+"}[1m])) by (name) * 100'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_cpu", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
            
                elif self.metrics[i] == 'TOTAL_BYTES_READS_CONTAINER':
                    # Métrica 3: Bytes Reads Total (B)
                    query = 'sum(rate(container_fs_reads_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_bytes_reads", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})
      
                elif self.metrics[i] == 'TOTAL_BYTES_WRITES_CONTAINER':
                    # Métrica 4: Bytes Writes Total (B/min)
                    query = 'sum(rate(container_fs_writes_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_bytes_writes", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

                elif self.metrics[i] == 'TOTAL_BYTES_RX_CONTAINER':
                    # Métrica 5: Bytes RX Total (B/min)
                    query = 'sum(rate(container_network_receive_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_bytesRX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

                elif self.metrics[i] == 'TOTAL_BYTES_TX_CONTAINER':
                    # Métrica 6: Bytes TX Total (B/min)
                    query = 'sum(rate(container_network_transmit_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_bytesTX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

                elif self.metrics[i] == 'TOTAL_PACKETS_RX_CONTAINER':
                    # Métrica 7: Packets RX Total (number)
                    query = 'sum(rate(container_network_receive_packets_total{name=~"[0-z]+"}[1m])) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_packetsRX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

                elif self.metrics[i] == 'TOTAL_PACKETS_TX_CONTAINER':
                    # Métrica 8: Packets TX Total (number)
                    query = 'sum(container_network_transmit_packets_total{name=~"[0-z]+"}) by (name)'
                    timestamp = datetime.now().timestamp()
                    PARAMS = {'query': query, 'time': timestamp}
                    print("Timestamp ", timestamp)
                    request = requests.get(url=URL, params=PARAMS)
                    metric = json.loads(request.text)
                    metrics.append(metric)
                    nResources = len(metrics[i]['data']['result'])
                    
                    for j in range(nResources):
                        resource_id = metrics[i]['data']['result'][j]['metric']['name']
                        resource_type = "Container"
                        value = metrics[i]['data']['result'][j]['value'][1]
                        timestamp = metrics[i]['data']['result'][j]['value'][0]
                        timestamp = datetime.fromtimestamp(timestamp).isoformat()

                        message.append({"measurement": "container_packetsTX_total", "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

            return message

initial_config = {'queue_user': 'slice', 'queue_password': 'slice', 'queue_port': '5672', 'vhost': 'slice'}
#data = json.dumps(sys.argv[1],separators=(',',':'))
data = sys.argv[1]
print(data)
update = eval(data)
initial_config.update(update)
print(initial_config)

while True:

    agent = agent_ima(json.dumps(initial_config,separators=(',',':')))
    message = agent.get_metrics()
    producer = agent_producer(json.dumps(initial_config,separators=(',',':')))
    producer.connection(message)
    time.sleep(int(initial_config['monitoring_interval']))
