from dotenv import load_dotenv
from os import environ


def load():
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
