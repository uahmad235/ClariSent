
from mongoengine import connect, ValidationError
from typing import List, Optional
from DataLayer.DBModel.ClauseLevelDetails import ClauseLevelDetail
from DataLayer.DBModel.FileDetails import FileDetail
from DataLayer.DBModel.Tokenizers import Tokenizer


class DBComm(object):
    """ manages db connection and read-write operations of DB"""

    def open_connection(self, db_name, **params):
        """ connects to a specified db name"""
        connect(db_name, **params)

    def insert_score_against_single_phrase(self, filename, phrase, score):
        pass

    def insert_score_against_complete_review(self, clauses_scores, _filename):

        _aggregated_score = 0

        clauses_list = []
        for _clause, _score, _sentiment_term_matched in clauses_scores:

            clauses_list.append(ClauseLevelDetail(clause = _clause , clause_score = _score,\
                                                  sentiment_term_matched = _sentiment_term_matched))
            _aggregated_score += _score

        try:
            FileDetail(filename = _filename, aggregated_score = _aggregated_score, clause_details_embedded = clauses_list)\
            .save()
        except ValidationError as err:

            # FileDetail.drop_collection()
            raise(Exception(err))


    def get_all_FileDetails_objs(self) -> Optional[List[FileDetail]]:

        if FileDetail.objects:
            return FileDetail.objects

    def get_all(self,collection_name):

        if collection_name == "FileDetails":
            return FileDetail.objects

    def write_tokenizers_to_db(self, file_path ):

        with open(file_path, 'r') as f:
            for line in f:
                Tokenizer(token = line.strip()).save()

    @staticmethod
    def read_sentiment_tokenizers_from_db():

        return [token.token for token in Tokenizer.objects]
