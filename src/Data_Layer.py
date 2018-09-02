
""" this file contains all the data access operations from Database/Files"""


class DataLayer(object):
    """ deals with the database read-write operations"""

    def read_sentiment_terms(self, path):
        """ read in all sentiments terms from a file and sorts them by length"""
        data = []
        with open(path, 'r') as f:
            for line in f.readlines():
                if line[:-3].strip() != "":
                    # -3 => sign, value, escape_character
                    data.append((line[:-3].strip(), line[-3:].strip()))

        print("Total No. of Sentiment Terms from '{}' read : {}".format(path, len(data)))
        sorted_st = self.sort_by_length(data)

        return sorted_st

    def sort_by_length(self, data):
        # sort by length for making trees
        return sorted(data, key=lambda x: len(x[0].split(' ')), reverse=False)

    @staticmethod
    def read_sentiment_tokenizers(path = "../data/tokenisers.txt"):
        """ read sentiment tokenizers for text tokenizing """

        tokenizers = []
        with open(path,'r') as f:
            for line in f:
                tokenizers.append(line.strip())

        return tokenizers