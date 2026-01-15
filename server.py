import socket

class Server:
    def __init__(self, port):
        self.port = port[0]
        self.server = None
        self.client = None
        self.client_message = None
        self.serv_message = None
    
    def server_client_connect(self) :
        self.server = socket.socket()
        self.server.bind(('0.0.0.0', self.port))
        self.server.listen()

        self.client, clinet_addr = self.server.accept()

        if clinet_addr:
            self.client_message = self.client.recv(1024)
            return  clinet_addr, self.client_message.decode()
    
    def server_message(self, message):
        self.serv_message = message

        self.client.sendall(self.serv_message.encode())
    
    def cli_message(self):
        
        client_message = self.client.recv(1024)

        return client_message.decode()
    def connection_close(self):
        self.server.close()

        return 'connection closed succesfully '
    
    
        

        
            

                        



        