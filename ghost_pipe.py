import argparse
from client import Client, GpChatClient
from server import Server, GroupChatServer
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

connect_group_chat = sub_command.add_parser('connect-groupchat')
connect_group_chat.add_argument('--addr', required=True, nargs=1, type=str)
connect_group_chat.add_argument('--port', type=int, required=True, nargs=1)
connect_group_chat.add_argument('-u', type=str, required=True, nargs=1)

listen_group_chat = sub_command.add_parser('listen-groupchat')
listen_group_chat.add_argument('--port', type=int, nargs=1, required=True)
listen_group_chat.add_argument('-u', type=str, nargs=1, required=True)


user_input = command.parse_args()

if user_input.mode == 'listen':
    server = Server(user_input.port, user_input.u)
    print(f'server started listening on port : {user_input.port}')
    clinett, clinet_addr = server.server_client_connect()
    if clinett:
        print(f'connected to {clinet_addr}')
        trd = threading.Thread(target=server.server_recv_msg)
        trd.start()
        
        server.server_snt_msg()

        server.serv_closing()
        
elif user_input.mode == 'connect':
    client = Client(user_input.addr, user_input.port, user_input.u)
    connection_result = client.clinet_server_connection()

    if connection_result:
        trd = threading.Thread(target=client.client_recv_msg)
        trd.start()

        client.clinet_snt_msg()

        client.clt_close()

elif user_input.mode == 'connect-groupchat':
    gp_cht_client = GpChatClient(user_input.addr, user_input.port, user_input.u)

    connection_result = gp_cht_client.client_gp_chat_connection()
    if connection_result:
        trd = threading.Thread(target=gp_cht_client.client_gp_cht_recv_msg)
        trd.start()
        gp_cht_client.client_gp_cht_snt_msg()
        gp_cht_client.client_gp_cht_connection_cls()
        
elif user_input.mode == 'listen-groupchat':
    gp_cht_server = GroupChatServer(user_input.port, user_input.u)

    trd = threading.Thread(target=gp_cht_server.connection)
    trd.start()
    gp_cht_server.gp_srvr_snt_msg()
    gp_cht_server.gp_chat_close()
    

elif user_input.mode == 'share':
    share_file = File_sender(user_input.addr, user_input.port, user_input.file)
    share_file.send_file()
elif user_input.mode == 'accept_file':
    recv_file = file_reciver(user_input.path, user_input.port)
    recv_file.recvfile()




        
        
        
        







