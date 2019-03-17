import select
import socket
import sys

from irc_chat_common_settings import PORT, INPUT_MESSAGE_LIMIT, EXIT_PROMPT, USER_NAME_INPUT_PROMPT

msg_prefix = ''

# provide a prompt to user to enter a message
def user_prompt():
    print('>>' + msg_prefix, end=' ', flush=True)

if len(sys.argv) < 2:
    print("Usage: python3 chat_client.py [hostname]", file=sys.stderr)
    sys.exit(1)
else:
    client_to_server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_to_server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client_to_server_connection.connect((sys.argv[1], PORT))
    except:
        print("!! Server unavailable !!", file=sys.stderr)
        sys.exit(1)

print('Successfully connected to Server!!')

socket_list = [sys.stdin, client_to_server_connection]

while True:
    # Get the list sockets which are readable
    # rlist: wait until ready for reading
    # wlist: wait until ready for writing
    # xlist: wait for an “exceptional condition”
    readlist, writelist, xlist = select.select(socket_list, [], [])

    for sock in readlist:
        if sock is client_to_server_connection:

            message = sock.recv(INPUT_MESSAGE_LIMIT)

            if not message:
                print('!!!Disconnected from IRC chat server!!!')
                sys.exit(2)
            else:
                if message == EXIT_PROMPT.encode():
                    sys.stdout.write(' Disconnecting now... I  gotta go\n')
                    sys.exit()
                else:
                    sys.stdout.write(message.decode())
                    if USER_NAME_INPUT_PROMPT in message.decode():
                        print('\n')
                        msg_prefix = 'nick_name: '
                    else:
                        msg_prefix = '' + " "
                    user_prompt()
        else:
            user_entered_msg = msg_prefix + sys.stdin.readline()
            client_to_server_connection.sendall(user_entered_msg.encode())
            user_prompt()
