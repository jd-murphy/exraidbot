
from socketIO_client import SocketIO

SocketIO socketIO

def on_connect():
    print('connected to https://node-bot-dashboard.herokuapp.com')

def on_disconnect():
    print('disconnect from https://node-bot-dashboard.herokuapp.com')

def on_reconnect():
    print('reconnected to https://node-bot-dashboard.herokuapp.com')

def on_aaa_response(*args):
    print('on_aaa_response', args)



def connect():
    print("Hello from socket.py")
    print("attempting to connect...")
    socketIO = SocketIO('https://node-bot-dashboard.herokuapp.com/')
    socketIO.on('connect', on_connect)
    socketIO.on('disconnect', on_disconnect)
    socketIO.on('reconnect', on_reconnect)
    socketIO.on('aaa_response', on_aaa_response)

    socketIO.emit('aaa')
    socketIO.emit('aaa')
    socketIO.wait(seconds=1)

    # Stop listening
    socketIO.off('aaa_response')
    socketIO.emit('aaa')
    socketIO.wait(seconds=1)

    socketIO.emit('notify')
   

def notify():
    print("Emitting 'notify'")
    socketIO.emit('notify')