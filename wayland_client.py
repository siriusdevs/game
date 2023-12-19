import evdev
import socket
from load_creds import load_address

keys_directions = {
    103: 'w',
    108: 's',
    105: 'a',
    106: 'd',
}


def get_keyboard():
    devices = [evdev.InputDevice(path)
               for path in reversed(evdev.list_devices())]

    for device in devices:
        capabilities = device.capabilities()
        if capabilities.get(1) and capabilities[1][0] == 1:
            return device


def keyboard_listener(device):
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            value = event.value
            if event.code in keys_directions.keys() \
               and (value == 0o01 or value == 0o02):
                client.send(keys_directions[event.code].encode())
            elif event == 1:
                client.send('q'.encode())
                client.close()
                break


client = socket.socket()
client.connect(load_address())


try:
    keyboard_listener(get_keyboard())
except KeyboardInterrupt:
    client.send('q'.encode())
    client.close()
