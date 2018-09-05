# setting python working environment

from src.SentimentTreesManager import *
from src.Utility_Functions import *
from src.DataLayer.Data_Layer import read_all_files_in_folder
from enum import Enum
from collections import Counter
from nltk.corpus import stopwords
from src.DataLayer.DBComm import DBComm


#  "not working->childOf->None" and "not working well->childOf->well" anomaly
# if we keep the sort order in alphabetic manner, we can keep this anomaly controlled
# let's see how:
# if alphabetically sorted, "not working well" will be somewhere next to "not working" and so "not working" will become
# parent and "not working well" will become it's child.


class NodeStatus(Enum):
    """ represents a node's status """
    pass

def split_on_spaces(text):
    return text.split(' ')


def main():
    """ entry point of the programme """

    trees_manager = SentimentTreesManager()

    sentiment_terms = DataLayer().read_sentiment_terms(path="../data/phone_st.txt")
    all_trees = trees_manager.make_trees(sentiment_terms)

    utils = UtilityFunctions(trees_manager)

    del sentiment_terms    # delete for the sake of memory :)

    folder_path = r"C:\Users\Usman Ahmad\Desktop\SA_Module\src\test-files-pos"  # for positive reviews

    counter = 0

    cnt = Counter()
    stop_words = set(stopwords.words('english'))

    for i,review_file in enumerate(read_all_files_in_folder(folder_path = folder_path)):

        filename = review_file[1]
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
        clauses_scores = utils.score_individual_piece_of_text(tokenized_text, all_trees[:])



    db_obj = DBComm()
    db_obj.open_connection(db_name= "ClariSent")
    # db_obj.insert_score_against_complete_review(clauses_scores, filename)

    pos, neg, neu = 0, 0, 0
    for i,x in enumerate(db_obj.get_all("FileDetails")):

        # print(x.filename, x.aggregated_score)
        # for c in x.clause_details_embedded:
        #     print(c.clause, c.clause_score)

        if x.aggregated_score == 0:
            print("Review #", i)
            for c in x.clause_details_embedded:
                print(c.clause, c.clause_score)
            neu += 1
        elif x.aggregated_score >0:
            pos += 1
        else:
            neg += 1

    print("Positive: {}, Negative: {}, Neutral: {}".format(pos, neg, neu))

    print("Accuracy: {}".format((pos+(neu//2))/(pos+neg+neu)))


    # print("total review-files found :{}".format(counter))

    for x in cnt.most_common(40):
        print(x, '  ',cnt[x])
    # tokenized_text = utils.split_string_with_multiple_tokenizers(review_1)
    # tokenized_text = map(lambda x: x.strip(), tokenized_text)
    #
    # utils.score_individual_piece_of_text(tokenized_text, all_trees[:])


    # print(list(tokenized_text))
    # utils.score_individual_piece_of_text(text=tokenized_text, sentiment_trees=all_trees)

    # for x in LevelOrderIter(all_trees[104]): #133
    #     # if x.is_leaf:
    #     # x.checked = True
    #     print(x.name, x.is_leaf)
    # print('*'*40)



if __name__ == "__main__":
    main()
