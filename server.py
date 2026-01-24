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
        self.file_path = None
        self.running = True
        self.quit_checker = None
    
    def server_client_connect(self) :
        try:
            
            self.server.bind(('0.0.0.0', self.port))
            self.server.listen()

            self.client, clinet_addr = self.server.accept()

            return self.client, clinet_addr
        
        except KeyboardInterrupt:
            print('keyboard intrepted , socket is closing ')
            self.server.close()
        except Exception as e:
            print(e)
    
    def server_server_message(self):
        while self.running:
            message = input('you : ')
            self.serv_message = self.user_name + ' : ' + message

            if not self.running:
             break
            
            if message == 'quit':
                
                self.client.sendall(self.cryptography.encrypt(self.serv_message.encode()))
                print('\nyou entered quit , the connection is terminating......', flush=True)
                self.running = False
                break
            self.client.sendall(self.cryptography.encrypt(self.serv_message.encode()))
        
        
    def server_cli_message(self):

        while self.running:

        
            client_message = self.client.recv(1024)
            if not self.running:
                break

            client_message_decrypted = self.cryptography.decrypt(client_message).decode()
            self.quit_checker = list(client_message_decrypted.split())
            if len(self.quit_checker) == 3 and self.quit_checker[2] == 'quit':
                self.running = False
                print(f'\n{client_message_decrypted}') 
                print('\n the connection is terminating ...',flush=True)
                
                break
            print(f'\n {client_message_decrypted}')
        
    def serv_closing(self):
        self.client.close()
        self.server.close()

    
        

        
            

                        



        