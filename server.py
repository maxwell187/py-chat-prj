from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s connected" % client_address)
        client.send(bytes("Connected.", "utf8"))
        addresses[client] = client_address
        Thread(target=clienthandler, args=(client,)).start()


def clienthandler(client): 

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! Type {quit} to quit' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 54813
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for a client connection.")
    ACCEPT_THREAD = Thread(target=incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
