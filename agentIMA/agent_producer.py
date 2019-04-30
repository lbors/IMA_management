import pika, sys
import json


class agent_producer():

    def __init__(self, initial_config):
        initial_config = json.loads(initial_config)
        self.user = initial_config['queue_user']
        self.password = initial_config['queue_password']
        self.ip = initial_config['slice_provider_ip']
        self.port_queue = initial_config['queue_port']
        self.vhost = initial_config['vhost']
        self.slice_id = initial_config['slice_id']
        self.queue_name = initial_config['slice_id']
        self.slicePartID = initial_config['slice_part_id']
        self.monitoring_tool = initial_config['monitoring_tool']
        self.monitoring_ip = initial_config['monitoring_ip']
        self.monitoring_port = initial_config['monitoring_port']
        self.interval = initial_config['monitoring_interval']
        self.metrics = initial_config['metrics']



    def connection(self, message):
        credentials = pika.PlainCredentials(self.user, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip, self.port_queue, self.vhost, credentials))
        channel = connection.channel()

        channel.queue_declare(queue=self.slice_id)

        channel.basic_publish(exchange='', routing_key=self.slice_id, body=str(message))
        print(" [x] Sent Metrics Message to Queue'")
        connection.close()
