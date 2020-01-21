import requests


class StackAPIConsumer:

    url = 'https://api.stackexchange.com/2.2/search'

    params = {
        'site': 'stackoverflow',
        'tagged': 'java',
    }

    @classmethod
    def consume(cls, data):
        cls.params.update(data)

