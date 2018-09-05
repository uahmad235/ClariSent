
from mongoengine import *

class Tokenizer(Document):

    token = StringField()

    meta = {

        'collection': 'Tokenizers'
    }