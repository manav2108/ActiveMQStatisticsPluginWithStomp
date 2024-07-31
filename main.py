import os,ssl
import time
import stomp
import xml.etree.ElementTree as ET

#Modify the below parameters
stompurl="b-5df792e6-5aee-4d67-94c7-4666c45d7275-2.mq.ap-southeast-1.amazonaws.com"
queueNameThatYouWantToQuery="queue1"
username='username'
password='password1234'
#do not modify the code below this line

def connect_and_subscribe(conn):
    conn.connect(username, password, wait=True)
    conn.subscribe(destination='/temp-queue/stat', id=1, ack='auto')

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        #print('received a message "%s"' % frame.body) #to get all the data, uncomment this line and parse XML
        root = ET.fromstring(frame.body)
        print("MessageCount="+root[13][1].text)
        
        for x in range(10):
            print(x)
            time.sleep(1)
        print('processed message')

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


conn = stomp.Connection([(stompurl, "61614")], auto_decode=True)
conn.set_ssl(for_hosts=[(stompurl, "61614")], ssl_version=ssl.PROTOCOL_TLS)
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
conn.send(body='', destination='ActiveMQ.Statistics.Destination.'+queueNameThatYouWantToQuery,headers={'reply-to': '/temp-queue/stat'} )
time.sleep(60)
conn.disconnect()
