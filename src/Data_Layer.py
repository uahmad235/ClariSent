
""" this file contains all the data access operations from Database/Files"""
import pandas as pd
import os


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


def process_pandas_chunk(chunk , counter = 1):
    """ process chunks """

    print("writing reviews to files...") # 28148
    for review in chunk["reviews"]:

        if type(review) is not float:
            if review.strip() == "":
                counter += 1; continue

            file_name = "./text-files-pos/file"+ str(counter) + ".txt"

            with open(file_name, 'w+', encoding="utf-8") as file:

                file.write(review)
            counter += 1

    return counter

def create_files_from_comments(path):

    if not path:
        print("Path must be provided")
        return


    c_size = 50000
    counter = 0
    # load the big file in smaller chunks
    for gm_chunk in pd.read_csv(path, chunksize=c_size):
        counter += process_pandas_chunk(gm_chunk, counter= counter)

        break


def create_files_from_file(read_path, counter = 1):

    with open(read_path) as file:

        # read
        for review in file:
            if type(review) is not float:
                if review.strip() == "":
                    counter += 1
                    continue

                file_name = "./test-files-neg/file" + str(counter) + ".txt"

                with open(file_name, 'w+', encoding="utf-8") as file:

                    file.write(review)
                counter += 1


def read_all_files_in_folder(folder_path):

    """ reads all files from folder for analysis"""

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)
        if not os.path.exists(file_path):
            print("path doesn't exists"); break


        with open(file_path, 'r') as file:

            review_from_file = file.read()[:-2].strip()
            yield (review_from_file, filename)

