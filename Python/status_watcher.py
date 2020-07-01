import requests
import time
from fbchat import Client, Message


URL = "http://www.cs.ubbcluj.ro/files/orar/2019-1/"
POOLING_WAIT = 60 
USERNAME = ""
PASSWORD = ""


def check_availability(url):
    print("Checking...")
    response = requests.get(url)
    while response.status_code != 200:
        print("not yet")
        time.sleep(POOLING_WAIT)
        response = requests.get(url)
    
    print("Orar - Available.")
    msg_text = "Orar is available now. Check it: " + URL
    notify_via_fb(USERNAME, PASSWORD, msg_text)


def notify_via_fb(username, password, msg):
    client = Client(username, password)

    found_users = client.searchForUsers("viorel.gurdis.7")
    user = found_users[0]

    # for user in client.fetchAllUsers():
    print("Sending message to:", user.first_name)
    client.send(Message(text=msg), thread_id=user.uid)

    client.logout()


check_availability(URL)