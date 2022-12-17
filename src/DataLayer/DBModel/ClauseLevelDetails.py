
from mongoengine import EmbeddedDocument
from mongoengine import fields
# keeps track Clause-Level Details

class ClauseLevelDetail(EmbeddedDocument):

    clause = fields.StringField()
    sentiment_term_matched = fields.StringField()
    clause_score = fields.IntField(min_value = -15, max_value = 15)

    meta = {
        'collection': 'ClauseLevelDetails'
    }
