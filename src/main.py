

# setting python working environment

from src.DataLayer import Data_Layer
from src.sentiment_trees import SentimentTreesManager
from src.utils import UtilityFunctions
from src.DataLayer.Data_Layer import read_all_files_in_folder
from collections import Counter
from nltk.corpus import stopwords
from src.DataLayer.DBComm import DBComm

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

    trees_manager = SentimentTreesManager()

    sentiment_terms = DataLayer().read_sentiment_terms(path="../data/phone_st.txt")
    all_trees = trees_manager.make_trees(sentiment_terms)

    utils = UtilityFunctions(trees_manager)
    aspects =  Data_Layer.read_aspects(path = r"C:\Users\Usman Ahmad\Desktop\SA_Module\data\Aspects.txt")

    del sentiment_terms    # delete for the sake of memory :)

    folder_path = r"C:\Users\Usman Ahmad\Desktop\SA_Module\src\test-files-pos"  # for positive reviews

    counter = 0

    db_obj = DBComm()
    db_obj.open_connection(db_name= "ClariSent")

    cnt = Counter()
    stop_words = set(stopwords.words('english')) # stop_words from nltk

    for i,review_file in enumerate(read_all_files_in_folder(folder_path = folder_path)):

        filename = review_file[1]  # review_file = tuple(review, filename)
        # if i == 10:
            # break
        # counter += 1
        tokenized_text = utils.split_string_with_multiple_tokenizers(review_file[0])

        for phrase in tokenized_text:
            for token in split_on_spaces(phrase):
                if token.lower() not in stop_words:
                    cnt[token] += 1

        tokenized_text = map(lambda x: x.strip(), tokenized_text)

        print("Review #" ,i)
        clauses_scores = utils.score_individual_piece_of_text(tokenized_text, all_trees[:], aspects= aspects)

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

    print("total review-files found :{}".format(counter))

    for x in cnt.most_common(40):
        print(x, '  ',cnt[x])




if __name__ == "__main__":
    main()
