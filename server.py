import socket
import threading
from tkinter import *


host = socket.gethostname()
port = 0


class ServerInterface(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.wm_title("Chatting - Server")
        self.wm_geometry("500x300")

        container = Frame(self)
        container.pack(fill=BOTH, expand=True)

        self.entry = Entry(container, state=DISABLED)
        self.entry.pack(side=BOTTOM, padx=6, pady=(0, 6), fill=X)

        self.textarea = Text(container)
        self.textarea.pack(side=TOP, padx=6, pady=6, fill=BOTH, expand=True)
        self.textarea.insert(END, "Waiting for connection...\n")
        self.textarea.insert(END, "Host: " + host + "\nPort Number: " + str(port) + "\n")

        self.setup_server()

    def setup_server(self):
        server = Server(self)
        server.daemon = True
        server.start()


class Server(threading.Thread):
    def __init__(self, controller):
        threading.Thread.__init__(self)

        global host, port

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


class AskPort(Tk):
    def __init__(self):
        Tk.__init__(self)

        global host

        self.wm_geometry("250x100")
        self.wm_title("Connection Configuration")

        container = Frame(self)
        container.pack(fill=BOTH, expand=True, padx=6, pady=6)

        container.columnconfigure(1, weight=1)

        label1 = Label(container, text="Host:")
        label1.grid(row=0, column=0)

        label2 = Label(container, text=host)
        label2.grid(row=0, column=1)

        label3 = Label(container, text="Port Number:")
        label3.grid(row=1, column=0)

        self.entry = Entry(container)
        self.entry.grid(row=1, column=1)
        self.entry.bind("<Return>", self.save)

        self.btn = Button(self, text="OK", command=self.save, width=5)
        self.btn.pack(side=BOTTOM, padx=6, pady=6)

    def save(self, *args):
        global port
        port_number = int(self.entry.get())
        port = port_number
        self.destroy()


if __name__ == '__main__':
    root = AskPort()
    root.mainloop()

    chatting = ServerInterface()
    chatting.mainloop()
