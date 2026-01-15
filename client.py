import socket

class Cient:
    def __init__(self, ip, port):
        self.server_addr = ip
        self.port = port[0]
        self.client_socket = None
        self.clinet_message = None
        self.server_message = None
        

    def clinet_server_connection(self) -> bool:

        self.client_socket = socket.socket()

        self.client_socket.connect((self.server_addr, self.port))
        print(f'client connected to {self.server_addr}')
        
        return True
    def clinet_server_chat(self, message):

        self.clinet_message = message

        self.client_socket.sendall(self.message.encode())
        self.server_message = self.client_socket.recv(1024)

        return self.server_message.decode()
    def clinet_socket_close(self):
        self.client_socket.close()
        return 'the connection closed '

    




    

        



        
        