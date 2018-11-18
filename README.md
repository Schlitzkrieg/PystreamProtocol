This project is something I started to learn more about messaging protocols that run on top of TCP sockets. I came across the need for something like this to aid in the development of my other project, “IM Secure Chat” (https://github.com/Schlitzkrieg/IMSecureChat-Server).

I am aware that other means of sending and receiving acks for data exists, so consider this project to be more along the lines of self-edification. I usually am against reinventing the wheel.

# Instructions
## Sending Data

```
from pystream import DataSender


sender = DataSender(socket_obj)
sender.send(message_obj)
```

## Receiving Data

```
from pystream import DataReceiver

rcvr = DataReceiver(socket_obj)
data_to_use = rcvr.receive()
# do something with data_to_use!
```
