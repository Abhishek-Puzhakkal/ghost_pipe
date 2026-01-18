import socket
from cryptography.fernet import Fernet

class Server:
    def __init__(self, port, username):
        self.key = b'l3d9jKgRTKAMWazsSKBsKmTAZ3x9RfeUdfi3zKbmDPI='
        self.cryptography = Fernet(self.key)
        self.user_name = username[0]
        self.port = port[0]
        self.server = socket.socket()
        self.client = None
        self.client_message = None
        self.serv_message = None
    
    def server_client_connect(self) :
        try:
            
            self.server.bind(('0.0.0.0', self.port))
            self.server.listen()

            self.client, clinet_addr = self.server.accept()

            if clinet_addr:
                self.client_message = self.client.recv(1024)
                client_decrypted_message = self.cryptography.decrypt(self.client_message)
                return  clinet_addr, client_decrypted_message.decode()
        except KeyboardInterrupt:
            print('keyboard intrepted , socket is closing ')
            self.server.close()
        except Exception as e:
            print(e)
    
    def server_message(self, message):
        self.serv_message = self.user_name + ' : ' + message

        self.client.sendall(self.cryptography.encrypt(self.serv_message.encode()))
    
    def cli_message(self):
        
        client_message = self.client.recv(1024)
        client_message_decrypted = self.cryptography.decrypt(client_message)

        return client_message_decrypted.decode()
    def connection_close(self):
        self.server.close()

        return 'connection closed succesfully '
    
    
        

        
            

                        



        