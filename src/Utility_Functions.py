
from Data_Layer import DataLayer
import re
import string
# from Main import has_unchecked_descendants
# from Main import get_unchecked_ultimate_descendants
from Main import *

class UtilityFunctions(object):


    def __init__(self):
        self.dataLayer = DataLayer()

    def analyse_text_for_sentiments(self):
        """ returns the analyzed strings for sentiment scores"""
        pass


    def compile_pattern_to_split(self):
        """ returns the compiled pattern to split string """

        regex_pattern = ""
        # r'\b'
        # regex_pattern +=  r'\b|\b'.join(map(re.escape, self.tokenizers)) + r'\b'

        for token in self.tokenizers:

            if token in string.punctuation:
                regex_pattern += re.escape(token) + r'|'
            else: # word
                regex_pattern += r'\b' + token + r'\b|'

        regex_pattern += r'\b\.'
        pattern = re.compile(regex_pattern, re.IGNORECASE)

        return pattern


    def split_string_with_multiple_tokenizers(self, text, tokenizers = None, path = "../data/tokenisers.txt"):
        """ splits text with given tokenizers """

        if not tokenizers and path:
            self.tokenizers = DataLayer.read_sentiment_tokenizers(path)

        pattern = self.compile_pattern_to_split()
        # filters empty values
        self.clauses = list(filter(None,(re.split(pattern, text))))

        return self.clauses


    def score_individual_piece_of_text(self ,text = None, sentiment_trees = None):

        if not text:
            text = self.clauses

        for clause in text:

            score = 0
            for tree in sentiment_trees:

                if has_unchecked_descendants(tree): # if tree has an unchecked descendant
                    unchecked_ultimate_descendants = get_unchecked_ultimate_descendants(tree)
                    # for each unchecked descendant
                    for unchecked_descendant in unchecked_ultimate_descendants:

                        # if tree's node is contained in clause
                        if first_in_second(unchecked_descendant.name, clause) and not unchecked_descendant.checked:
                            score += int(unchecked_descendant.value)
                            set_all_ancestors_checked(unchecked_descendant) # mark all ancestors checked


            print("clause: {}\n Score agaist clause: {}".format(clause, score))