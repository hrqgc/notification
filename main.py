from simplegmail import Gmail
from simplegmail.query import construct_query
import re

gmail = Gmail()

query_params = {
    "newer_than":(3,"hour"),
    # "unread": True,
    # "labels":[["Work"],["Homework","CS"]]
}

messages = gmail.get_messages(query=construct_query(query_params))
pattern = re.compile(r'Customer:\s*(.*)', re.IGNORECASE)


for message in messages:
    if message.plain:
        match= pattern.search(message.plain)
        if match:
            print(f'AAAAAAAAAAAAA {match.group(1).strip()} \n\n\n\n\n\n\n\n\n')


    print(f"to: {message.recipient}\n")
    print(f"from: {message.sender}\n")
    print(f"subject: {message.subject}\n")
    print(f"date: {message.date}\n")
    print(f"preview: {message.snippet}\n")
    print(f"body: {message.plain}\n")