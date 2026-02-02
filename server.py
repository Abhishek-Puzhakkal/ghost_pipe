import socket
from cryptography.fernet import Fernet
import threading


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
    
    def server_snt_msg(self):
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
        
        
    def server_recv_msg(self):

        while self.running:

            try :
                client_message = self.client.recv(1024)
            except OSError as e :
                if e.winerror in (10053, 10054):
                    print('The connection closed peacefully...')
                else:
                    raise
            except Exception as e :
                print(e)
                
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


class GroupChatServer:
    def __init__(self, port, username):
        self.gp_chat_svr_socket = socket.socket()
        self.port = port[0]
        self.username = username[0]
        self.clients_socket = None
        self.clients_addr = None
        self.server_running = True
        self.clients_dict = dict()
        self.quict_checker = list()
    def connection(self):
        self.gp_chat_svr_socket.bind(('0.0.0.0', self.port))
        self.gp_chat_svr_socket.listen()
        
        print('\nserver started listening.....')
        def server_brodcast(client):
            try : 
                
                while self.server_running:
                    sender = client
                    
                    
                    if not self.server_running:
                        break
                    try:
                        client_message = client.recv(1024).decode()
                    except OSError as e:
                        if e.winerror in (10053, 10054):
                            pass
                        else:
                            raise
                    if not client_message:
                        break
                    if not self.server_running:
                        break
                
                    
                    
                    
                    broadcasting_flag = 'broadcasting'
                    
                    if client_message and len(self.clients_dict) >= 2:
                        self.quict_checker = client_message.split()
                        username = self.quict_checker[0]
                        if len(self.quict_checker) == 3 and self.quict_checker[2] == 'quit':
                            broadcasting_message = broadcasting_flag + ' ' + client_message
                            print(f'\n{client_message}')
                            print(f'\n{username} quit, so that connection is closing...')
                            for clients in self.clients_dict:
                                if clients == sender:
                                    pass
                                else:
                                    clients.sendall(broadcasting_message.encode())
                            
                            client.close()
                            self.clients_dict.pop(client)
                            print(f' \nnow the remaining members in group chat : {len(self.clients_dict)}')
                            break
                        
                        else:
                              
                            print(f'\n{client_message}')
                            broadcasting_message = broadcasting_flag + ' ' + client_message
                            for clients in self.clients_dict:
                                if clients == sender:
                                    pass
                                else:
                                    clients.sendall(broadcasting_message.encode())
                                    
                    elif client_message and len(self.clients_dict) < 2:
                        self.quict_checker = client_message.split()
                        
                        if len(self.quict_checker) == 3 and self.quict_checker[2] == "quit":
                            print(f'\n{client_message}')
                            print('\nthe entire connection is closing....')
                            self.server_running = False
                            break
                        else:
                            print(f'\n{client_message}')
            except KeyboardInterrupt:
                print('\nkeyboard intrepted....')
            except Exception as e:
                print(e)
           

        while self.server_running:
            try:

                clients_socket, clients_addr = self.gp_chat_svr_socket.accept()
            except OSError as e:
                if not self.server_running:
                    break
                else:
                    raise
            if clients_socket:
                if clients_socket not in self.clients_dict:
                    print(f'\nnew connection arrived , {clients_addr} ')
                    self.clients_dict[clients_socket] = clients_addr
                    threading.Thread(target=server_brodcast, args=(clients_socket,)).start()
                    
    def gp_srvr_snt_msg(self):
        try : 
            server_message_flag = 'admin'
            while self.server_running :
                server_message = input('\nyou : ')
                if not self.server_running:
                    break
                server_message_broadcast = server_message_flag + ' ' + self.username + ' : '+ server_message
                
                if server_message == 'quit':
                    self.server_running = False
                    for clients in self.clients_dict:
                        clients.sendall(server_message_broadcast.encode())
                    print('you enterd quit , connection going to terminate....')
                    
                    break
                for clients in self.clients_dict:
                    clients.sendall(server_message_broadcast.encode())
        except KeyboardInterrupt:
            print('keyboard interpted....')
        except Exception as e:
            print(e)
                
    def gp_chat_close(self):
        for clients in self.clients_dict:
            clients.close()
        self.gp_chat_svr_socket.close()
        print('entire connection closed peacefully....')



    

        

        
            

                        



        