# CS594-Internet Relay Chat
This project demonstrates the use of a multi-client IRC chat application

The server and the client have been written in [Python3](https://docs.python.org/3/). The previous versions of python
    are not supported.

We have references the module [Interprocess Communication and Networking](https://docs.python.org/3/library/ipc.html)
    for allowing us to enable a communication among clients 

We have tried to follow the best practices for python projects[Python best practices](http://docs.python-guide.org/en/latest/writing/structure/)

In regards to following best practices we took an approach to make use of markdown files to document some of our work

# Authors:
- [Payal Joshi](https://github.com/payaljoshi0189)

- [Geetam Pathak]()

# FAQ

Q. What is IRC?

Ans: Please refer here for more details[IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat)

Q. How to start the server?

Ans: Open a new terminal window, and if you are using `python3`, please use the following command:
```
python3 chat_server.py 127.0.0.1
```
you will see a message such as:
```
Server listening on 22222, is now ready to receive messages
```

Q. How to start a client?

Ans: Open up a new terminal window for a client, and then use the following command

```
python3 chat_client.py 127.0.0.1
```
After that the client will be prompted to enter a `nick_name`, this can be any string.
The following will be the display for a client
```
Successfully connected to Server!!
To start chatting, please enter a nick name.


>>nick_name:  payal
>>nick_name:  What can I do?:
[_j channel_name] to create/join/switch channel e.g _j psu
[_l] Command to list existing channels\ e.g: _l psu 
[list_users channel_name] Command to list existing channels e.g: list_users psu
[_h] Command to display all the options available.
[leave channel_name] Command to leave a channel e.g: leave psu
[exit] to exit from chat application
```

Q: What is a nick name?
Ans: As per the RFC document[nick name](https://tools.ietf.org/html/rfc7700), it is used as a human-friendly name
of the user joining a chat room

Q: What is a channel?

Ans: A channel is a chat room

Q: What are the features supported by your IRC chat application?
Ans: Currently, we have the following features that are supported
1. A Server process, i.e. able to start a server on a localhost and a port 2222
2. Currently we support upt to a maximum of 30 clients to be able to connect to a single server
3. A client has the ability to create a room
4. A client can list all the rooms
5. A client can join a room
6. A client can leave a room
7. A client can join multiple rooms
8. A client can send distinct messages to multiple chat rooms
9. A client can list members of a chat room
10. A client can disconnect from  a server
11. Server can disconnect from all clients
12. A server can gracefully handle client crashes
13. A client can gracefully handle server crashes    

You can find more details in `RFC` document provided under the `/docs` folder

#References:
[1]. https://en.wikipedia.org/wiki/Internet_Relay_Chat

[2]. http://docs.python-guide.org/en/latest/writing/structure/

[3]. https://docs.python.org/3/library/select.html

[4]. https://docs.python.org/3/

[5]. https://docs.python.org/3/library/ipc.html

[6]. https://en.wikipedia.org/wiki/Markdown

[7]. https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
