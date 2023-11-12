import socket
from threading import Thread 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipAddress="127.0.0.1"
port=8000
server.bind((ipAddress, port))
server.listen()
listOfClients=[]
nicknames=[]
print("Server has started...")
def clientThread(connection, nickname):
    connection.send("Welcome to this chatroom".encode("utf-8"))
    while True:
        try:
           message=connection.recv(2048).decode("utf-8")
           if message:
               print(message)
               messageToSend=message
               broadcast(messageToSend, connection)
           else:
               remove(connection)
               remove_nickname(nickname)
        except:
            continue
def broadcast(message, connection):
    for client in listOfClients:
        if client!=connection:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove(client)
def remove(connection):
    if connection in listOfClients:
        listOfClients.remove(connection)
def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)
while True:
    connection,address=server.accept()
    connection.send("NICKNAME".encode("utf-8"))
    nickname=connection.recv(2048).decode("utf-8")
    listOfClients.append(connection)
    nicknames.append(nickname)
    message="{} join".format(nickname)
    print(message)
    broadcast(message, connection)
    newThread=Thread(target=clientThread, args=(connection, nickname))
    newThread.start()