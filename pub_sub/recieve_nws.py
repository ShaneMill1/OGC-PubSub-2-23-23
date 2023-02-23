#!/opt/conda/envs/env/bin/python

import pika
import sys
from datetime import datetime
import requests

credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters('ec2-18-117-219-29.us-east-2.compute.amazonaws.com',5672,'/',credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.exchange_declare(exchange='edr', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='edr', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting to recieve messages. To exit press CTRL+C')



def callback(ch, method, properties, body):
    time=datetime.now().isoformat()
    if isinstance(body,str) != True:
       body=body.decode('utf-8')
    print("[x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
