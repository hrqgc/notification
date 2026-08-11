from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os
from simplegmail import Gmail
from simplegmail.query import construct_query
import json
import re
from banco import cursor, conexao
import sqlite3
import threading

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fcivil-tube-501812-q1-aae53e85c03b.json'

project_id = "civil-tube-501812-q1"
subscription_id = "heythere"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

gmail = Gmail()
travar_banco = threading.Lock()

def addBanco():
    with travar_banco:
        query_params = {
            'newer_than':(1,"hour"),
            'unread':True
        }

        new_email = gmail.get_messages(query=construct_query(query_params))

        pattern = re.compile(r'Customer:\s*(.*)', re.IGNORECASE)
        for email in new_email:
            print('email 1')
            if email.plain:
                print('email 2')
                match= pattern.search(email.plain)
                if match:
                    costumer_name = match.group(1).strip()
                    print(f'email 3 {costumer_name}')
                    cursor.execute('''INSERT INTO requests (name) VALUES(?)''', (costumer_name,))
                    conexao.commit()



            print(email.subject)
            email.mark_as_read()



def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f'Received message: {message}')
    message.ack()
    addBanco()





streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()