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
        self.running = True
        self.quit_checker = list()
        

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
    def clinet_clinet_message(self):
        while self.running:
            message = input('you : ')
            if not self.running:
                break

            if message: 

                if not self.running:
                    break


                if message == 'quit':
                    

                    self.clinet_message = self.username + ' : '+ message

                    self.client_socket.sendall(self.cryptography.encrypt(self.clinet_message.encode()))
                    print(f'\nyou entered "quit", connection is terminating....', flush=True)
                    self.running = False
                    
                    break
                    
                    
                
                self.clinet_message = self.username + ' : '+ message

                self.client_socket.sendall(self.cryptography.encrypt(self.clinet_message.encode()))
                

        '''self.client_socket.close()'''


    def client_server_message(self):

        while self.running:
            servermessage = self.client_socket.recv(1024)
            

            if not self.running:
                
                break

            if servermessage:
                self.server_message = self.cryptography.decrypt(servermessage).decode()
                
            
                if not self.running:
                    
                    break
                
                self.quit_checker = self.server_message.split()

                if len(self.quit_checker) == 3 and self.quit_checker[2] == 'quit':
                    
                    print(f'\n{self.server_message}')
                    print('\nthe connection is terminating....', flush=True)
                    self.running = False
                    break
                print(f'\n{self.server_message}')

        '''self.client_socket.close()'''

    def clt_close(self):
        self.client_socket.close()




    




    

        



        
        