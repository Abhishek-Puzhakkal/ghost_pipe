import argparse
from client import Cient
from server import Server

command = argparse.ArgumentParser()
sub_command = command.add_subparsers(dest='mode', required=True)

connect_command = sub_command.add_parser('connect')
connect_command.add_argument('--addr', required=True, nargs=1, )
connect_command.add_argument('--port', type=int, required=True, nargs=1)

listent_command = sub_command.add_parser('listen')
listent_command.add_argument('--port', type=int, required=True, nargs=1)


user_input = command.parse_args()

if user_input.mode == 'listen':
    server = Server(user_input.port)
    print(f'server started listening on port : {user_input.port}')
    clinet_addr, clinet_message = server.server_client_connect()
    if clinet_addr:
        print(f'connected to {clinet_addr}')
        while True:
            if clinet_message == 'quit':
                connection_close = server.connection_close()
                print(connection_close)
                break
            elif clinet_message:
                print(f'{clinet_addr} : {clinet_message}')
                message = input('you : ')
                server.server_message(message)
                clinet_message = server.cli_message()

elif user_input.mode == 'connect':
    client = Cient(user_input.addr, user_input.port)
    connection_result = client.clinet_server_connection()

    if connection_result == True:
        print(f'connecntion succesfull now you ant start chat ')
        while True:
            message = input('you : ')
            server_message = client.clinet_server_chat(message)
            if server_message == 'quit':
                connection_close = client.clinet_socket_close()
                print(connection_close)
                break
            elif server_message:
                print(f"{user_input.addr} : {server_message}")



        
        
        
        







