import requests


class StackAPIQuestion:
    tags = []
    owner = {}
    is_answered = False
    view_count = None
    answer_count = None
    score = None
    last_activity_date = None
    creation_date = None
    last_edit_date = None
    question_id = None
    link = None
    title = None

    def __init__(self, data):
        print(data)
        print(type(data))
        self.tags = data['tags']
        self.owner = data['owner']
        self.is_answered = data['is_answered']
        self.view_count = data['view_count']
        self.answer_count = data['answer_count']
        self.score = data['score']
        self.last_activity_date = data['last_activity_date']
        self.creation_date = data['creation_date']
        if 'last_edit_date' in data.values():
            self.last_edit_date = data['last_edit_date']
        self.question_id = data['question_id']
        self.link = data['link']
        self.title = data['title']

    def __str__(self):
        return self.title


class StackAPIConsumer:

    url = 'https://api.stackexchange.com/2.2/search'

    params = {
        'site': 'stackoverflow',
        'tagged': 'java',
    }

    @classmethod
    def consume(cls, data):
        cls.params.update(data)
        r = requests.get(cls.url, params=cls.params)
        return r

