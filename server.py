import socket
import threading
from tkinter import *


class ServerInterface(Tk):
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
        self.textarea.insert(END, "Waiting for connection...\n")

        self.setup_server()

    def setup_server(self):
        server = Server(self)
        server.daemon = True
        server.start()


class Server(threading.Thread):
    def __init__(self, controller):
        threading.Thread.__init__(self)

        self.entry = controller.entry
        self.textarea = controller.textarea

        self.s = socket.socket()
        host = socket.gethostname()
        port = 12345
        self.s.bind((host, port))
        self.s.listen(5)

    def run(self):
        while True:
            client, addr = self.s.accept()
            self.entry.bind("<Return>", lambda x: self.send_message(client))
            show_message("connected from: " + str(addr), self.textarea)
            self.entry["state"] = NORMAL
            ReceiveMessageThread(client, self.textarea).start()

    def send_message(self, client):
        message = self.entry.get()
        if message:
            self.entry.delete(0, END)
            client.send(message)
            show_message("Server: " + message, self.textarea)


class ReceiveMessageThread(threading.Thread):
    def __init__(self, client, textarea):
        threading.Thread.__init__(self)

        self.client = client
        self.textarea = textarea

    def run(self):
        while True:
            try:
                message = self.client.recv(1024)
                show_message("Client: " + message, self.textarea)
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
    chatting = ServerInterface()
    chatting.mainloop()
