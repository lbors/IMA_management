from pprint import pprint
from influxdb import InfluxDBClient
import json

class database():

    def insert_data(self, user, data, ip):
        print(user)
        print(ip)
        client = InfluxDBClient(host=ip, port=8086)
        client.switch_database(str(user))
        print(client.get_list_database())

        data = str(data,'utf-8')
        data = data.replace('\'','\"')

        print(data)
        json_array = json.loads(str(data))
        print(json_array)

        client.write_points(json_array)

    def create_database(self, user, ip):
        client = InfluxDBClient(host=ip, port=8086)
        client.create_database(str(user))
