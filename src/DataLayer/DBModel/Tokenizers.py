
from mongoengine import Document
from mongoengine.fields import StringField

class Tokenizer(Document):

    token = StringField()

    meta = {

        'collection': 'Tokenizers'
    }