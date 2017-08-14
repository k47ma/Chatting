import socket
import threading


class Server(object):
    def __init__(self):
        object.__init__(self)
        self.s = socket.socket()
        host = socket.gethostname()
        port = 12345
        self.s.bind((host, port))
        self.s.listen(5)
        self.wait_for_client()

    def wait_for_client(self):
        while True:
            print "waiting for connection..."
            client, addr = self.s.accept()
            print "connected from:", addr
            ReceiveMessageThread(client).start()
            SendMessageThread(client).start()


class ReceiveMessageThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            try:
                message = self.client.recv(1024)
                print "Client: " + message
            except Exception:
                break


class SendMessageThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        while True:
            try:
                message = raw_input()
                self.client.send(message)
                print "Server: " + message
            except Exception:
                break
