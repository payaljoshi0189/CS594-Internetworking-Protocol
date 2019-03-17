#Class to hold information about all the clients
class ChatUser:
    def __init__(self, socket, current_channel_name="", nickname="newUser"):
        socket.setblocking(0)
        self.socket = socket
        self.nickname = nickname
        self.current_channel_name = current_channel_name
        self.member_of = []     # A dictionary of channels, the  client is part of

    # Return socket's file descriptor or -1 in case of error
    def fileno(self):
        return self.socket.fileno()