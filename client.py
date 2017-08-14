import socket
import threading
from tkinter import *


class ClientInterface(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.wm_title("Chatting")
        self.wm_geometry("500x300")

        container = Frame(self)
        container.pack(fill=BOTH, expand=True)

        self.entry = Entry(container, state=DISABLED)
        self.entry.pack(side=BOTTOM, padx=6, pady=(0, 6), fill=X)

        self.textarea = Text(container)
        self.textarea.pack(side=TOP, padx=6, pady=6, fill=BOTH, expand=True)

        self.setup_server()

    def setup_server(self):
        client = Client(self)
        client.daemon = True
        client.start()


class Client(threading.Thread):
    def __init__(self, controller):
        threading.Thread.__init__(self)

        self.entry = controller.entry
        self.textarea = controller.textarea

    def run(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        try:
            s.connect((host, port))
        except Exception:
            show_message("Can't connect to the server!", self.textarea)
            return

        self.entry["state"] = NORMAL
        self.entry.bind("<Return>", lambda x: self.send_message(s))

        show_message("connected to: " + str(socket.getaddrinfo(host, port)[1][-1]), self.textarea)
        ReceiveMessageThread(s, self.textarea).start()

    def send_message(self, connection):
        message = self.entry.get()
        if message:
            self.entry.delete(0, END)
            connection.send(message)
            show_message("Client: " + message, self.textarea)


class ReceiveMessageThread(threading.Thread):
    def __init__(self, connection, textarea):
        threading.Thread.__init__(self)

        self.connection = connection
        self.textarea = textarea

    def run(self):
        while True:
            try:
                message = self.connection.recv(1024)
                show_message("Server: " + message, self.textarea)
            except Exception:
                break


class ShowMessage(threading.Thread):
    def __init__(self, message, textarea):
        threading.Thread.__init__(self)
        self.message = message
        self.textarea = textarea

    def run(self):
        self.textarea.insert(END, self.message)
        self.textarea.see(END)


def show_message(message, textarea):
    thread = ShowMessage(message + "\n", textarea)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    client = ClientInterface()
    client.mainloop()
