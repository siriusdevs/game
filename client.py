import socket
from load_creds import load_address
from pynput import keyboard


client = socket.socket()
client.connect(load_address())

keys_directions = {
    keyboard.Key.up: 'w',
    keyboard.Key.down: 's',
    keyboard.Key.left: 'a',
    keyboard.Key.right: 'd',
}

def on_press(key: str):
    if key in keys_directions:
        try:
            client.send(keys_directions[key].encode())
        except ConnectionError:
            print('Вы были отключены от сервера!')
            return
    elif key == keyboard.Key.esc:
        client.send('q'.encode())
        client.close()
        return


listener = keyboard.Listener(on_press=on_press)
try:
    listener.start()
except KeyboardInterrupt:
    client.send('q'.encode())
    client.close()

listener.join()

