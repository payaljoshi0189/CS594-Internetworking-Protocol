import select
import socket
import sys

from chat_user import ChatUser
from irc_chat_functions import WelcomeScreen

from irc_chat_common_settings import PORT, MAX_CLIENTS, INPUT_MESSAGE_LIMIT

host = sys.argv[1] if len(sys.argv) >= 2 else ''

def create_socket(address):
    socket_util = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # To avoid error 'address in use', let the kernel reuse a local socket in TIME_WAIT state
    socket_util.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set the socket to non-blocking mode so as to avoid waiting for operation completion
    socket_util.setblocking(0)

    socket_util.bind(address)

    socket_util.listen(MAX_CLIENTS)

    return socket_util


welcome = WelcomeScreen()
INCOMING_CONNECTIONS = []

server_socket = create_socket((host, PORT))

INCOMING_CONNECTIONS.append(server_socket)

print("Server listening on " + str(PORT) + ", is now ready to receive messages."+ "\n")

while True:

    readlist, writelist, xlist = select.select(INCOMING_CONNECTIONS, [], [])
    try:
        for user in readlist:
            if user == server_socket:       # New connection
                new_user_socket, address = server_socket.accept()
                user = ChatUser(new_user_socket)
                INCOMING_CONNECTIONS.append(user)
                welcome.add_user(user)

            else:       # New message
                message = user.socket.recv(INPUT_MESSAGE_LIMIT)
                if message:
                    message = message.decode().lower()
                    welcome.process_user_messages(user, message)

                else:
                    # if any problem occurs on the client side, server will just remove the client
                    user.socket.close()
                    INCOMING_CONNECTIONS.remove(user)
    except:
        for sock in xlist:
            print("Disconnecting user: " + sock.nickname)
            sock.close()
            INCOMING_CONNECTIONS.remove(sock)

