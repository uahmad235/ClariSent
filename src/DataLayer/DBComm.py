
from mongoengine import *

from src.DataLayer.DBModel.ClauseLevelDetails import ClauseLevelDetail
from src.DataLayer.DBModel.FileDetails import FileDetail


class DBComm(object):
    """ manages db connection and read-write operations of DB"""


    def open_connection(self, db_name = None):
        """ connects to a specified db name"""
        connect(db_name)


    def insert_score_against_single_phrase(self, filename, phrase, score):
        pass


    def insert_score_against_complete_review(self, clauses_scores, _filename):

        _aggregated_score = 0

        clauses_list = []
        for _clause, _score in clauses_scores:

            clauses_list.append(ClauseLevelDetail(clause = _clause , clause_score = _score))
            _aggregated_score += _score

        try:
            FileDetail(filename = _filename, aggregated_score = _aggregated_score, clause_details_embedded = clauses_list)\
            .save()
        except ValidationError as err:

            # FileDetail.drop_collection()
            raise(Exception(err))



    