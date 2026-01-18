import socket
from cryptography.fernet import Fernet

class Cient:
    def __init__(self, ip, port, username):
        self.key = b'l3d9jKgRTKAMWazsSKBsKmTAZ3x9RfeUdfi3zKbmDPI='
        self.cryptography = Fernet(self.key)
        self.username = username[0]
        self.server_addr = ip[0]
        self.port = port[0]
        self.client_socket = socket.socket()
        self.clinet_message = None
        self.server_message = None
        

    def clinet_server_connection(self) -> bool:
        try:
            

            self.client_socket.connect((self.server_addr, self.port))
            print(f'client connected to {self.server_addr}')
            
            return True
        except KeyboardInterrupt:
            print('keyboard intrpted ')
            self.client_socket.close()
        except Exception as e:
            print(e)
    def clinet_server_chat(self, message:str):

        if message != 'quit':

            self.clinet_message = self.username + ' : '+ message

            self.client_socket.sendall(self.cryptography.encrypt(self.clinet_message.encode()))
            self.server_message = self.cryptography.decrypt(self.client_socket.recv(1024))
            
            if self.server_message:

                return self.server_message.decode()
        else :
            self.clinet_message = self.username + ' : '+ message

            self.client_socket.sendall(self.cryptography.encrypt(self.clinet_message.encode()))

    def clinet_socket_close(self):
        self.client_socket.close()
        return 'the connection closed '

    




    

        



        
        