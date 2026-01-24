import argparse
from client import Cient
from server import Server
from file_sharing import file_reciver, File_sender
import threading

command = argparse.ArgumentParser()
sub_command = command.add_subparsers(dest='mode', required=True)

connect_command = sub_command.add_parser('connect')
connect_command.add_argument('--addr',type=str, required=True, nargs=1, )
connect_command.add_argument('--port', type=int, required=True, nargs=1)
connect_command.add_argument('-u', required=True, type=str, nargs=1)

listent_command = sub_command.add_parser('listen')
listent_command.add_argument('--port', type=int, required=True, nargs=1)
listent_command.add_argument('-u', required=True, type=str, nargs=1)

share_file_command = sub_command.add_parser('share')
share_file_command.add_argument('--port', type=int, required=True, nargs=1)
share_file_command.add_argument('--addr', required=True, nargs=1)
share_file_command.add_argument('--file', nargs=1, required=True)

accept_file_command = sub_command.add_parser('accept_file')
accept_file_command.add_argument('--path',required=True, nargs=1 )
accept_file_command.add_argument('--port', required=True, nargs=1, type=int)


user_input = command.parse_args()

if user_input.mode == 'listen':
    server = Server(user_input.port, user_input.u)
    print(f'server started listening on port : {user_input.port}')
    clinett, clinet_addr = server.server_client_connect()
    if clinett:
        print(f'connected to {clinet_addr}')
        trd = threading.Thread(target=server.server_cli_message, daemon=True)
        trd.start()
        
        server.server_server_message()
        trd.join()

        server.serv_closing()
        
elif user_input.mode == 'connect':
    client = Cient(user_input.addr, user_input.port, user_input.u)
    connection_result = client.clinet_server_connection()

    if connection_result:
        trd = threading.Thread(target=client.client_server_message, daemon=True)
        trd.start()

        
        client.clinet_clinet_message()

        trd.join()

        client.clt_close()
        

elif user_input.mode == 'share':
    share_file = File_sender(user_input.addr, user_input.port, user_input.file)
    share_file.send_file()
elif user_input.mode == 'accept_file':
    recv_file = file_reciver(user_input.path, user_input.port)
    recv_file.recvfile()




        
        
        
        







