
# this file will store details of an individual file

from mongoengine import *

from src.DataLayer.DBModel.ClauseLevelDetails import ClauseLevelDetail


class FileDetail(Document):


    filename = StringField(unique=True)
    aggregated_score = IntField()
    clause_details_embedded = EmbeddedDocumentListField(ClauseLevelDetail)

    meta = {

        'collection' : 'FileDetails',
        'indexes' : ['filename']

    }