from DataLayer.data_layer import DataLayer
import re
import string
import sentiment_trees as ST


class UtilityFunctions(object):

    def __init__(self, trees_manager, aspects, tokenizer_path):
        # self.dataLayer = DataLayer()
        self.trees_manager = trees_manager
        self.aspects = aspects
        self.tokenizers = DataLayer.read_sentiment_tokenizers(tokenizer_path)

    def analyse_text_for_sentiments(self):
        """ returns the analyzed strings for sentiment scores"""
        pass

    @staticmethod
    def first_in_second(first, second):
        """ returns true if the first string is contained in second string"""
        compiled_regex = re.compile(r"\b(%s)\b" % (first), re.IGNORECASE)
        objects = re.search(compiled_regex, second)
        if objects:
            return True
        return False

    def compile_pattern_to_split(self):
        """ returns the compiled pattern to split string """

        regex_pattern = ""
        for token in self.tokenizers:
            if token in string.punctuation:
                regex_pattern += re.escape(token) + r'|'
            else: # word
                regex_pattern += r'\b' + token + r'\b|'

        regex_pattern += r'\b\.'
        pattern = re.compile(regex_pattern, re.IGNORECASE)

        return pattern

    def split_string_with_multiple_tokenizers(self, text):
        """ splits text with given tokenizers """
        pattern = self.compile_pattern_to_split()
        # filters empty values
        self.clauses = list(filter(None,(re.split(pattern, text))))

        return self.clauses


    def _match_aspects(self, clause):
        
        regex_pattern = ""
        for token in self.aspects:
            regex_pattern += r'\b' + token + r'\b|'
        regex_pattern += r'\b\.'
        pattern = re.compile(regex_pattern, re.IGNORECASE)
        matched_aspects = list(filter(None,(re.finditer(pattern, clause))))
        return list(set([aspect.group() for aspect in matched_aspects]))

    def score_individual_piece_of_text(self ,text = None, sentiment_trees = None):
        """ scores individual text/File/multiple-clauses """

        if not text:
            print("Didn't get text")
            text = self.clauses

        clause_score = []

        for clause in text:

            sentiment_term_matched = ""
            score = 0
            aspects_per_clause = {}

            for tree in sentiment_trees:

                if ST.SentimentTreesManager.has_unchecked_descendants(tree): # if tree has an unchecked descendant
                    unchecked_ultimate_descendants = ST.SentimentTreesManager.get_unchecked_ultimate_descendants(tree)
                    # for each unchecked descendant
                    for unchecked_descendant in unchecked_ultimate_descendants:
                        # if tree's node is contained in clause
                        if UtilityFunctions.first_in_second(unchecked_descendant.name, clause) and\
                                                                not unchecked_descendant.checked:
                            score += int(unchecked_descendant.value)
                            ST.SentimentTreesManager.set_all_ancestors_checked(unchecked_descendant) # mark all ancestors checked
                            sentiment_term_matched = unchecked_descendant.name
                            # Find the aspect in the clause and tie it to the matched sentiment-term 
                            matched_aspects = self._match_aspects(clause)
                            if matched_aspects:
                                aspects_per_clause[sentiment_term_matched] = matched_aspects 

            print("aspects/clause:: ", aspects_per_clause)
            clause_score.append((clause, score, aspects_per_clause))  # append clauses against their scores
            print("clause: {} --> Score : {} -> term : {}, {}".format(clause, score, aspects_per_clause, sentiment_term_matched))

        # reset all trees for next clause match
        self.trees_manager.reset_all_trees()
        return clause_score
