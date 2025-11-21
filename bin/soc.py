import socket
from threading import Thread


class Server_soc(Thread):
    def __init__(self, port=2222, *args, **kwags):
        # implement the setup here
        
        super().__init__(*args, **kwags)



class Client_soc(Thread):
    def __init__(self, s_port=2222, s_ip=None, *args, **kwags):
        # implement the code setup here

        super().__init__(*args, **kwags)


