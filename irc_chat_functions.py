from chat_channel import ChatChannel

from irc_chat_common_settings import EXIT_PROMPT

# class to present all available options to members entering the irc chat room
class WelcomeScreen:
    options_available = b'What can I do?:\n' \
                        + b'[_j channel_name] to create/join/switch channel e.g _j psu\n'\
                        + b'[_l] Command to list existing channels\ e.g: _l psu \n'\
                        + b'[list_users channel_name] Command to list members of the channel e.g: list_users psu\n' \
                        + b'[_h] Command to display all the options available.\n' \
                        + b'[leave channel_name] Command to leave a channel e.g: leave psu\n' \
                        + b'[exit] to exit from chat application\n' \

    def __init__(self):
        self.channels = {} # this list for all the channels created by all the clients
        self.channel_user_map = {} # map of a user associated to a channel_name

    # To initiate adding of users
    def add_user(self, new_user):
        new_user.socket.sendall(b'To start chatting, please enter a nick name.\n')

    # To list all available channels
    def list_all_channels(self, user):
        available_chatrooms = ''
        channels_joined = ''

        if len(self.channels) == 0:
            status_message = 'No channels available to join. You can create a channel using the command:\n' \
                  + ' [_j channel_name].\n'
            user.socket.sendall(status_message.encode())
        else:
            status_message = 'Channels available\n'

            # List all the currently available channels
            for channel in self.channels:
                available_chatrooms += channel + ": " + str(len(self.channels[channel].users)) + " user(s)\n"

            user.socket.send(status_message.encode())
            user.socket.send(available_chatrooms.encode())

            # List all the channels that a client is member of
            if len(user.member_of) == 0:
                status_message = "Currently you are not a part of any channel.\n"
                user.socket.sendall(status_message.encode())
            else:
                for channel_name in user.member_of:
                    channels_joined += channel_name + "\n"
                user.socket.sendall("You are a member of.\n".encode())
                user.socket.sendall(channels_joined.encode())

    # assign a nick name to a new user
    def assign_nickname(self, user, message):
        nickname = message.split()[1]
        user.nickname = nickname
        user.socket.sendall(self.options_available)
        print("User: ", str(nickname) + " joined.")

    # to create/join a new/existing channel
    def join_chat_channel(self, user, message):
        if len(message.split()[0]) == 2 and len(message.split()) == 2:
            channel_name = message.split()[1]

            if channel_name in self.channels:                                           # Channel exists
                if channel_name in user.member_of:                                      # User is already a member of requested channel
                    user.current_channel_name = channel_name                            # Point current channel name to requested channel
                    self.channel_user_map[user.nickname] = channel_name
                else:                                                                   # User is not member of this channel
                    self.channels[channel_name].users.append(user)                      # Add the user to the list of users for channel
                    self.channel_user_map[user.nickname] = channel_name                 # Add mapping to user_channel mapping dictionary
                    user.current_channel_name = channel_name                            # Point current channel name to requested channel
                    user.member_of.append(self.channels[channel_name])                  # Add channel to the list of channels for user
                    self.channels[user.current_channel_name].joined_channel(user)       # Inform the user about addition of new member
            else:                                                                       # Channel does not exist

                new_channel = ChatChannel(channel_name)                                 # Create new channel
                self.channels[channel_name] = new_channel                               # Add to the channels list
                self.channels[channel_name].users.append(user)                          # Add this user to the the list of users of channel
                user.current_channel_name = channel_name                                # Point current channel name to requested channel
                self.channel_user_map[user.nickname] = channel_name                     # Add mapping to user_channel mapping dictionary
                user.member_of.append(new_channel)                                     # Add channel to the list of channels for user
                self.channels[channel_name].joined_channel(user)
        else:
            errormessage = "This is an incorrect command to join a channel. Please type _j channel_name"
            user.socket.send(errormessage.encode())

    # to display the user options
    def display_options(self, user):
        user.socket.send(self.options_available)

    # To quit chat application but still able
    def quit_application(self, user):
        # Remove user's entry from channel_user_map
        if user.nickname in self.channel_user_map:
            del self.channel_user_map[user.nickname]
            print(user.nickname + " left (:")

        # Delete user from each channel's users list
        for channel in user.member_of:
            channel.left_channel(user)

        user.socket.sendall(EXIT_PROMPT.encode())

    # Method to handle all the messages sent by users
    def continue_chatting(self, user, msg):
        if msg:
            if user.nickname in self.channel_user_map:
                self.channels[self.channel_user_map[user.nickname]].send_message_to_all(user, msg.encode())
        else:
            msg = b'Hey chat user!! you are not in any channel \n'
            user.socket.sendall(msg)

    # user remove themselves from a specific channel they are member of
    def user_leave_a_channel(self, user, message):
        channel_name = message.split()[1]
        channel = self.channels[channel_name]

        # Check if user is member of this channel
        if channel_name in self.channel_user_map[user.nickname]:
            channel.left_channel(user)
            if user.nickname in self.channel_user_map:
                del self.channel_user_map[user.nickname]
                print(user.nickname + " left (:")
            else:
                errormessage = "Error, you are not a member of " + channel_name
                user.socket.send(errormessage.encode())
        else:
            errormessage = "Error, you are not a member of "+ channel_name
            user.socket.send(errormessage.encode())

    # Method to list all the members in a given channel
    def channel_members (self,user, message):
        if len(message.split()[0]) == 10 and len(message.split()) == 2:
            channel_name = message.split()[1]
            users = "Available users in "+channel_name+" are:\n"
            for member in self.channels[channel_name].users:
                users += member.nickname + "\n"
            user.socket.send(users.encode())
        else:
            errormessage = "This is an incorrect command to list channel members. Please type [list_users channel_name].\n"
            user.socket.send(errormessage.encode())


    # Method to handle all the messages sent by users
    def process_user_messages(self, user, message):
        if "nick_name" in message:
            self.assign_nickname(user, message)

        elif "_j" in message:
            self.join_chat_channel(user, message)

        elif '_l' in message:
            self.list_all_channels(user)

        elif 'list_users' in message:
            self.channel_members(user,message)

        elif '_h' in message:
            self.display_options(user)

        elif 'leave' in message:
            self.user_leave_a_channel(user, message)

        elif 'exit' in message:
            self.quit_application(user)

        else:
            self.continue_chatting(user, message)