#Class to hold information about all the channels
class ChatChannel:
    def __init__(self, channel_name):
        self.users = []  # a list of sockets
        self.channel_name = channel_name

    # Display message to all the users, if a new user joins channel
    def joined_channel(self, sender):
        message = sender.nickname + " joined " + self.channel_name + '\n'
        for user in self.users:
            user.socket.sendall(message.encode())

    def resumed_channel(self, sender):
        message = sender.nickname + " resumed " + self.channel_name + '\n' + 'Welcome back!!'+ '\n'
        for user in self.users:
            user.socket.sendall(message.encode())

    # send message to all the users who are members of the channel
    def send_message_to_all(self, sender, message):
        message = sender.nickname.encode() + b":" + message
        for user in self.users:
            user.socket.sendall(message)

    # remove user from the list of users when user leaves a channel
    def left_channel(self, user):
        self.users.remove(user)
        user.member_of.remove(self)
        leave_msg = user.nickname.encode() + b" left\n"
        self.send_message_to_all(user, leave_msg)