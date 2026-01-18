import argparse
from client import Cient
from server import Server

command = argparse.ArgumentParser()
sub_command = command.add_subparsers(dest='mode', required=True)

connect_command = sub_command.add_parser('connect')
connect_command.add_argument('--addr',type=str, required=True, nargs=1, )
connect_command.add_argument('--port', type=int, required=True, nargs=1)
connect_command.add_argument('-u', required=True, type=str, nargs=1)

listent_command = sub_command.add_parser('listen')
listent_command.add_argument('--port', type=int, required=True, nargs=1)
listent_command.add_argument('-u', required=True, type=str, nargs=1)


user_input = command.parse_args()

if user_input.mode == 'listen':
    server = Server(user_input.port, user_input.u)
    print(f'server started listening on port : {user_input.port}')
    clinet_addr, clinet_message = server.server_client_connect()
    if clinet_addr:
        print(f'connected to {clinet_addr}')
        while True:
            print('123')
            
            quit_checker = list(clinet_message.split())
            print(quit_checker)
            if len(quit_checker) == 3 and quit_checker[2] == 'quit':
                connection_close = server.connection_close()
                print(connection_close)
                break
            elif clinet_message:
                print(f'{clinet_message}')
                message = input('you : ')
                server_side_quit_checker = list(message.split())

                if len(server_side_quit_checker) == 1 and server_side_quit_checker[0] == 'quit' :
                    print('server side inside while loop elif block wokring')
                    server.server_message(message)
                    connection_close = server.connection_close()
                    print('connection closed peace fully...')
                    break
                else:
                
                    server.server_message(message)
                    clinet_message = server.cli_message()

elif user_input.mode == 'connect':
    client = Cient(user_input.addr, user_input.port, user_input.u)
    connection_result = client.clinet_server_connection()

    if connection_result == True:
        print(f'connecntion succesfull now you can start chat ')
        while True:
            message = input('you : ')
            quit_checker = list(message.split())
            server_message = client.clinet_server_chat(message)
            if server_message:
                server_side_quit_checker = list(server_message.split())
                if len(server_side_quit_checker) == 3 and server_side_quit_checker[2] == 'quit':

                    connection_close = client.clinet_socket_close()
                    print(connection_close)
                    print('client code if worked ')
                    break
                elif server_message:
                    print(f"{server_message}")
            elif len(quit_checker) == 1 and quit_checker[0] == 'quit' :

                connection_close = client.clinet_socket_close()
                print(connection_close)
                print('clinet code 2nd elif code workde')
                break
            



        
        
        
        







