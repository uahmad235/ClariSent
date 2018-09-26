
from mongoengine import *
# keeps track Clause-Level Details

class ClauseLevelDetail(EmbeddedDocument):

    clause = StringField()
    sentiment_term_matched = StringField()
    clause_score = IntField(min_value = -15, max_value = 15)

    meta = {
        'collection': 'ClauseLevelDetails'
    }
