import pika, sys
import slice_database
import json


class slice_aggregator():
    #file = open(sys.argv[1], 'r')
    #line = file.read().splitlines()

    def __init__(self, initial_config):
        initial_config = json.loads(initial_config)
        self.user = initial_config['queue_user']
        self.password = initial_config['queue_password']
        self.ip = initial_config['slice_provider_ip']
        self.port_queue = initial_config['queue_port']
        self.vhost = initial_config['vhost']
        self.slice_id = initial_config['slice_id']
        self.queue_name = initial_config['slice_id']

    def rabbit_connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip, self.port_queue, self.vhost, credentials))
        channel = connection.channel()

        return channel

    def create_database(self, db):
        db.create_database(self.slice_id, self.ip)

    def create_queue(self, channel, db):
        def callback(ch, method, properties, body):
            print(" [x] Received data ")
            db.insert_data(self.slice_id, body, self.ip)

        print(self.queue_name)
        channel.queue_declare(queue=self.queue_name)

        channel.basic_consume(callback, queue=self.queue_name, no_ack=True)

        print(' [*]Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


initial_config = {'queue_user': 'slice', 'queue_password': 'slice', 'queue_port': '5672', 'vhost': 'slice'}
#data = json.dumps(sys.argv[1],separators=(',',':'))
data = sys.argv[1]
print(data)
update = eval(data)
initial_config.update(update)
print(initial_config)
consumer = slice_aggregator(json.dumps(initial_config,separators=(',',':')))
channel = consumer.rabbit_connection()
db = slice_database.database()
consumer.create_database(db)
consumer.create_queue(channel, db)
