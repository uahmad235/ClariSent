
# this file will store details of an individual file

from mongoengine import Document, EmbeddedDocumentListField
from mongoengine import fields

from DataLayer.DBModel.ClauseLevelDetails import ClauseLevelDetail


class FileDetail(Document):

    filename = fields.StringField()
    aggregated_score = fields.IntField()
    clause_details_embedded = EmbeddedDocumentListField(ClauseLevelDetail)

    meta = {

        'collection' : 'FileDetails',
        'indexes' : ['filename']

    }