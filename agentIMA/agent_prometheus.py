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

    def collect_metrics_physical(self):
        if self.monitoring_tool == 'prometheus':
            URL = "http://%s:%s/api/v1/query?" % (self.monitoring_ip, self.monitoring_port)
            print(URL)
            physical_metric = []

            # Métrica 1: Physical Memory used by node (%)
            query = '((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Memory Node: %s\n" % metric)

            # Métrica 2: Physical CPU used by node (%)
            query = '100 - (avg by (host) (irate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric CPU Node: %s\n" % metric)

            # Métrica 3: Bytes Reads Total (B)
            query = 'sum(node_disk_reads_completed_total) by (host)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Bytes Reads Node: %s\n" % metric)

            # Métrica 4: Bytes Writes Total (B)
            query = 'sum(node_disk_writes_completed_total) by (host)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Bytes Writes Node: %s\n" % metric)

            # Métrica 5: Bytes RX Total (B)
            query = 'sum(node_network_receive_bytes_total) by (host)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Bytes Received Node: %s\n" % metric)

            # Métrica 6: Bytes TX Total (B)
            query = 'sum(node_network_transmit_bytes_total) by (host)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Bytes Transmited Node: %s\n" % metric)

            # Métrica 7: Packets TX Total (number)
            query = 'sum(node_network_transmit_packets_total) by (host)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Packets Transmited Node: %s\n" % metric)

            # Métrica 8: Packets RX Total (number)
            query = 'sum(node_network_receive_packets_total) by (host)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            physical_metric.append(metric)
            print("Metric Packets Received Node: %s\n" % metric)

            return physical_metric

    def collect_container_metrics(self):
        if self.monitoring_tool == 'prometheus':
            URL = "http://%s:%s/api/v1/query?" % (self.monitoring_ip, self.monitoring_port)
            print(URL)
            container_metric = []

            # Métrica 1: Container Memory used (B)
            query = 'sum(container_memory_usage_bytes{name=~"[0-z]+"}) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Memory Container: %s\n" % metric)

            # Métrica 2: Container CPU used (%)
            query = 'sum(rate(container_cpu_usage_seconds_total{name=~"[0-z]+"}[1m])) by (name) * 100'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric CPU Container: %s\n" % metric)

            # Métrica 3: Bytes Reads Total (B)
            query = 'sum(rate(container_fs_reads_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Bytes Reads Container: %s\n" % metric)

            # Métrica 4: Bytes Writes Total (B/min)
            query = 'sum(rate(container_fs_writes_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Bytes Writes Container: %s\n" % metric)

            # Métrica 5: Bytes RX Total (B/min)
            query = 'sum(rate(container_network_receive_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Bytes Received Container: %s\n" % metric)

            # Métrica 6: Bytes TX Total (B/min)
            query = 'sum(rate(container_network_transmit_bytes_total{name=~"[0-z]+"}[1m])) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Bytes Transmited Container: %s\n" % metric)

            # Métrica 7: Packets RX Total (number)
            query = 'sum(rate(container_network_receive_packets_total{name=~"[0-z]+"}[1m])) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Packets Received Container: %s\n" % metric)

            # Métrica 8: Packets TX Total (number)
            query = 'sum(container_network_transmit_packets_total{name=~"[0-z]+"}) by (name)'
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metric = json.loads(request.text)
            container_metric.append(metric)
            print("Metric Packets Transmited Container: %s\n" % metric)

            return container_metric

    def parser_metrics_container(self, metrics):
        nMetrics = len(metrics)

        string = list()
        #kpi_name = ['container_memory (B)', 'container_cpu (%)', 'container_bytes_reads (B)', 'container_bytes_writes (B)', 'container_bytesRX_total (B)', 'container_bytesTX_total (B)', 'container_packetsRX_total (counter)', 'container_packetsTX_total (counter)']
        kpi_name = ['container_memory', 'container_cpu', 'container_bytes_reads', 'container_bytes_writes', 'container_bytesRX_total', 'container_bytesTX_total', 'container_packetsRX_total', 'container_packetsTX_total']

        for i in range(nMetrics):
            nResources = len(metrics[i]['data']['result'])
            #print(nResources)
            for j in range(nResources):
                resource_id = metrics[i]['data']['result'][j]['metric']['name']
                resource_type = "Container"
                value = metrics[i]['data']['result'][j]['value'][1]
                timestamp = metrics[i]['data']['result'][j]['value'][0]
                timestamp = datetime.fromtimestamp(timestamp).isoformat()
                string.append({"measurement": kpi_name[i], "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

        print(string)
        return string

    def parser_metrics_physical(self, metrics):
        nMetrics = len(metrics)
        #kpi_name = ['node_memory (B)', 'node_cpu (%)', 'node_bytes_reads (B)', 'node_bytes_writes (B)', 'node_bytesRX_total (B)', 'node_bytesTX_total (B)', 'node_packetsRX_total (counter)', 'node_packetsTX_total (counter)']
        kpi_name = ['node_memory', 'node_cpu', 'node_bytes_reads', 'node_bytes_writes', 'node_bytesRX_total', 'node_bytesTX_total', 'node_packetsRX_total', 'node_packetsTX_total']
        string = list()

        for i in range(nMetrics):
            nResources = len(metrics[i]['data']['result'])
            for j in range(nResources):
                resource_id = metrics[i]['data']['result'][j]['metric']['host']
                resource_type = "Physical"
                value = metrics[i]['data']['result'][j]['value'][1]
                timestamp = metrics[i]['data']['result'][j]['value'][0]
                timestamp = datetime.fromtimestamp(timestamp).isoformat()

                string.append({"measurement": kpi_name[i], "tags": {"resource_id": resource_id, "resource_type": resource_type, "slice_id": self.slice_id, "slice_part_id": self.slice_part_id}, "time": timestamp, "fields": {"value": value}})

        print(string)
        return string


initial_config = {'queue_user': 'slice', 'queue_password': 'slice', 'queue_port': '5672', 'vhost': 'slice'}
#data = json.dumps(sys.argv[1],separators=(',',':'))
data = sys.argv[1]
print(data)
update = eval(data)
initial_config.update(update)
print(initial_config)

while True:

    agent = agent_ima(json.dumps(initial_config,separators=(',',':')))
    container_metrics = agent.collect_container_metrics()
    message_container = agent.parser_metrics_container(container_metrics)

    physical_metrics = agent.collect_metrics_physical()
    message_physical = agent.parser_metrics_physical(physical_metrics)

    producer = agent_producer(json.dumps(initial_config,separators=(',',':')))
    producer.connection(message_container)
    producer.connection(message_physical)
    time.sleep(int(initial_config['monitoring_interval']))
