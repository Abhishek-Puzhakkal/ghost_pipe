import socket
from cryptography.fernet import Fernet
from pathlib import Path
from tqdm import tqdm

class File_sender():
    def __init__(self, addr, port, file_path):
        self.key = b'5BH7FCe5mrbIMGbebcuy3wg9PCjhsk3_qqVqZbtuU4s='
        self.addr = addr[0]
        self.port = port[0]
        self.file_path = file_path[0]
        self.sender_socket = socket.socket()
    
    def send_file(self):
        path_of_file = Path(self.file_path).expanduser()
        file_encryption = Fernet(self.key)

        if path_of_file.is_file():
            file_size = path_of_file.stat().st_size

            self.sender_socket.connect((self.addr, self.port))
            print('connection succesfull....')

            self.sender_socket.sendall(str(file_size).encode())

            with open(path_of_file, 'rb') as file:
                p_bar = tqdm(total=file_size, unit='B', unit_scale=True)

                while True:

                    file_chunk = file.read(1024)
                    

                    if not file_chunk:
                        break

                    encrypted_file_chunk = file_encryption.encrypt(file_chunk)
                    self.sender_socket.sendall(encrypted_file_chunk)
                    p_bar.update(len(file_chunk))
                p_bar.close()
                print('file sharing completed...')
            self.sender_socket.close()
        else:
            print(f'{self.file_path} is not a file or not exist  in machine')


class file_reciver():
    def __init__(self, file_path, port):
        self.key = b'5BH7FCe5mrbIMGbebcuy3wg9PCjhsk3_qqVqZbtuU4s='
        self.port = port[0]
        self.file_path = file_path[0]
        self.recever_socket = socket.socket()
    
    def recvfile(self):
        filepath = Path(self.file_path).expanduser()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        file_decryption = Fernet(self.key)
        if not filepath.exists():
            self.recever_socket.bind(('0.0.0.0', self.port))
            self.recever_socket.listen()
            file_sender, file_sender_addr = self.recever_socket.accept()

            if file_sender:
                print(f'machine connected to {file_sender_addr}')
                file_size = int(file_sender.recv(1024).decode())
                with open(filepath, 'wb') as file:
                    p_bar = tqdm(total=file_size, unit='B', unit_scale=True)

                    while True:

                        file_chunk = file_sender.recv(1024)
                       
                        if not file_chunk:
                            break

                        decrypted_file_chunk = file_decryption.decrypt(file_chunk)
                        file.write(decrypted_file_chunk)
                        p_bar.update(len(file_chunk))
                    
                    p_bar.close()
                    print('file received completely...')
            self.recever_socket.close()
        else:
            print(f'{self.file_path} alredy exist in machine, to recv the file you need a empty file or a new file ')



        

            


        