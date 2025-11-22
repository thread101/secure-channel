#!/usr/bin/python3

import socket
import threading
import sys
import os
from time import localtime, time


# general functions and variables
tym = lambda: str(f"[{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec}]")

def handle_error(func):
    def wrapper(*args, **kwags):
        try:
            r = func(*args, **kwags)
        
        except Exception as e:
            r = f"[error] {e}"

        return r
    return wrapper

def printTerminal(text:str, mode:str="recv", title:str|None=None):
    '''
        formating text to the console for a better look and feel.
        titled --> for printing errors and headings
        else:
            modes:
                recv --> printing received text
                sent --> printing sent text
    '''
    global timeStamp, tym
    terminal_length = os.get_terminal_size().columns
    format_ratio = 0.7
    formated_text = ""

    if len(text) == 0:
        return
    
    if title is not None:
        
        title = f" <{title}> "
        x = (terminal_length - len(title))//2
        formated_text += f"{'-'*x}{title}{'-'*x}"

        y = (terminal_length - len(text))//2
        formated_text += f"\n{' '*y}{text}"

        formated_text += f"\n{'-'*terminal_length}"

    else:
        words = text.split()
        x = int(terminal_length*format_ratio) + 3

        if len(text) + 2 < x:
            x = len(text) + 4
            padding_left = terminal_length - (x + 2)
            if mode == "recv":
                formated_text += f"@{'-'*x}+\n"
                formated_text += f"| {text}{' '*(x-len(text)-1)}|\n"
                formated_text += f"+{'-'*x}+\n"

            else:
                formated_text += f"{' '*padding_left}+{'-'*x}@\n"
                formated_text += f"{' '*padding_left}| {text}{' '*(x-len(text)-1)}|\n"
                formated_text += f"{' '*padding_left}+{'-'*x}+\n"

        else:
            padding_left = int(terminal_length*(1-format_ratio)) - 4

            if mode == "recv":
                formated_text += f"@{'-'*x}+\n"

                line = f"| {words[0]}"
                for word in words[1:]:
                    word = f" {word}"
                    if len(line + word) + 2 < x:
                        line += word

                    else:
                        formated_text += f"{line} {' '*(x-len(line))}|\n"
                        line = f"|{word}"

                formated_text += f"{line} {' '*(x-len(line))}|\n"
                formated_text += f"+{'-'*x}+\n"

            else:
                formated_text += f"{' '*padding_left}+{'-'*x}@\n"

                line = f"| {words[0]}"
                for word in words[1:]:
                    word = f" {word}"
                    if len(line + word) + 2 < x:
                        line += word

                    else:
                        formated_text += f"{' '*padding_left}{line} {' '*(x-len(line))}|\n"
                        line = f"|{word}"

                formated_text += f"{' '*padding_left}{line} {' '*(x-len(line))}|\n"
                formated_text += f"{' '*padding_left}+{'-'*x}+\n"

        if timeStamp:
            t = tym()
            formated_text += f"{t}\n" if mode == "recv" else f"{' '*(terminal_length-len(t))}{t}\n"

    print(f"\r{formated_text}\ntype: ", end=" ")
    
def inputTerminal():
    while True:
        print("\rtype: ", end=" ")
        msg = input()

        if len(msg) == 0:
            continue

        printTerminal(text=msg, mode="sent")
        return msg

# server specific functions
@handle_error
def send(client:socket.socket, msg:str):
    msg = msg.encode("utf-8")
    client.send(msg)
    return 0

@handle_error
def recv(client:socket.socket):
    message = client.recv(1024).decode("utf-8")
    return message

def receiver(client:socket.socket):
    global tym

    while True:
        msg = recv(client)

        if len(msg) == 0:
            printTerminal(text="Client offline", title="Error")
            break

        printTerminal(text=msg, mode="recv")

def server(port:int=8000):
    global tym

    s = socket.socket()
    s.bind(("", port))

    printTerminal(text="Waiting for connection...", title="Log")
    s.listen(1)

    client = s.accept()[0]
    threading.Thread(target=receiver, args=(client,)).start()

    printTerminal(text=f"session started at: {tym()}", title="Log")

    while True:
        message = inputTerminal()

        r = send(client, message)

        if r != 0:
            printTerminal(text=r, title="Error")


# client specific functions
@handle_error
def c_send(server:socket.socket, msg:str):
    msg = msg.encode("utf-8")
    server.send(msg)
    return 0

@handle_error
def c_recv(server:socket.socket):
    msg = server.recv(1024).decode("utf-8")
    return msg

def c_receiver(server:socket.socket):
    global tym

    while True:
        msg = c_recv(server)

        printTerminal(text=msg, mode="recv")

def client(ip:str="", port:int=8000):
    global tym

    c = socket.socket()
    try:
        c.connect((ip, port))
        threading.Thread(target=c_receiver, args=(c,)).start()
        printTerminal(text=f"session started at: {tym()}", title="Log")
        isOnline = True
    
    except ConnectionRefusedError:
        printTerminal(text="server not online...", title="Log")
        isOnline = False

    while isOnline:
        message = inputTerminal()

        r = c_send(c, message)

        if r != 0:
            printTerminal(text=r, title="Error")

if __name__ == "__main__":
    timeStamp = False
    try:
        mode = sys.argv[1]
        try:
            timeStamp = bool(sys.argv[2])

        except IndexError:
            pass
    
    except IndexError:
        mode = input("input the mode\n\t[s] (server) \n\t[c] (client)\n>>> ")

    if "s" in mode:
        printTerminal(text="server mode initiated", title="Log")
        server()

    else:
        printTerminal(text="client mode initiated", title="Log")
        client()