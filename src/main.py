

# setting python working environment

from DataLayer import data_layer
from sentiment_trees import SentimentTreesManager
from utils import UtilityFunctions
from DataLayer.data_layer import read_all_files_in_folder
from collections import Counter
from nltk.corpus import stopwords
from DataLayer.db_comm import DBComm
import os


SENTIMENT_TERMS_PATH = "data/phone_st.txt"
ASPECTS_PATH = "data/aspects_phone.txt"
DB_NAME = "ClariSent"
EVAL_DIR = "data/eval"  # directory to evaluate sentiments from
TOKENIZER_PATH = "data/tokenisers.txt"


"""
"not working->childOf->None" and "not working well->childOf->well" anomaly
if we keep the sort order in alphabetic manner, we can keep this anomaly controlled
let's see how:
if alphabetically sorted, "not working well" will be somewhere next to "not working" and so "not working" will become
parent and "not working well" will become it's child.
"""

def split_on_spaces(text):
    return text.split(' ')


def main():
    """ entry point of the programme """

    db_obj = DBComm()
    auth = {"username": os.environ['USERNAME'], "password": os.environ['PASSWORD']}
    db_obj.open_connection(db_name=DB_NAME, **auth)
    
    trees_manager = SentimentTreesManager()
    
    sentiment_terms = data_layer.DataLayer().read_sentiment_terms(path=SENTIMENT_TERMS_PATH)
    all_trees = trees_manager.make_trees(sentiment_terms)

    aspects =  data_layer.read_aspects(path = ASPECTS_PATH)
    utils = UtilityFunctions(trees_manager, aspects, TOKENIZER_PATH)

    del sentiment_terms    # delete for the sake of memory :)

    cnt = Counter()
    stop_words = set(stopwords.words('english')) # stop_words from nltk

    for i, (filename, review) in enumerate(read_all_files_in_folder(folder_path = EVAL_DIR)):

        tokenized_text = utils.split_string_with_multiple_tokenizers(review)

        for phrase in tokenized_text:
            for token in split_on_spaces(phrase):
                if token.lower() not in stop_words:
                    cnt[token] += 1

        tokenized_text = map(lambda x: x.strip(), tokenized_text)

        print("Review #", i)
        clauses_scores = utils.score_individual_piece_of_text(tokenized_text, all_trees[:])

        db_obj.insert_score_against_complete_review(clauses_scores, filename)

    pos, neg, neu = 0, 0, 0
    for i,x in enumerate(db_obj.get_all("FileDetails")):

        if x.aggregated_score == 0:
            print("Review #", i)
            for c in x.clause_details_embedded:
                print(c.clause, c.clause_score)
            neu += 1
        elif x.aggregated_score > 0:
            pos += 1
        else:
            neg += 1

    print("Positive: {}, Negative: {}, Neutral: {}".format(pos, neg, neu))

    print("Accuracy: {}".format((pos+(neu//2))/(pos+neg+neu)))

    for x in cnt.most_common(40):
        print(x, '  ',cnt[x])




if __name__ == "__main__":
    main()
