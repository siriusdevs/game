from dotenv import load_dotenv
from os import environ


def load_address():
    load_dotenv()
    return (
        environ.get(
            'HOST', 
            default='127.0.0.1',
        ),
        int(
            environ.get(
            'PORT',
            default=4321,
            )
        )
    )

def load_size():
    load_dotenv()
    return (
        int(
            environ.get(
                'WIDTH', 
                default=120,
            )
        ),
        int(
            environ.get(
                'HEIGHT',
                default=80,
            )
        )
    )
