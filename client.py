import socket
import threading


class Client(object):
    def __init__(self):
        object.__init__(self)
        self.s = socket.socket()
        host = socket.gethostname()
        port = 12345
        self.s.connect((host, port))
        print "connected to:", socket.getaddrinfo(host, port)[1][-1]
        ReceiveMessageThread(self.s).start()
        SendMessageThread(self.s).start()


class ReceiveMessageThread(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        while True:
            message = self.connection.recv(1024)
            print "Server: " + message


class SendMessageThread(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        message = raw_input()
        self.connection.send(message)
        print "Client: " + message
