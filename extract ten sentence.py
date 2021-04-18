import sys
import csv

from computeARIintoANewLastColumn import readfile

# TODO:
#       document code properly, and also testing
#           remember to document each class and function, with complexity, input, return, etc
#           (btw need ot double check if preconditions are documented correctly)
#           error handling//catching, such as try and except
### the use of "###" in comments indicates the comment is means as a NOTE, or a possible place to TEST, or A PROBLEM
### THAT NEEDS ADDRESSING



# Extra code limitation: "....." is


def main_function(dataset_file_name):
    """
    This functions extracts only the first 10 sentence in the csv only, and returns the data now holding
     only 10 sentences.
    :precondition: dataset must be .csv
                   the text data must be in the last row for our dataset
    :param dataset_file_name: the .csv dataset's file name
    :return: tuple (header, data)
                WHERE
                    header is the first header row to be added to our output csv in list format

                    data is the rows to be added to our output csv in list format, and each row in data
                    represents a document
    """

    # read our csv file
    header, data = readfile(dataset_file_name)

    # m is the index of the last cell of in a row
    # we assume all row are has the same number of columns in the CSV
    m = len(data[0]) - 1

    # note that each row is assumed to represent a document
    # for each document, tokenize its text
    the_extracted = []
    for row in data:
        text = row[m]
        row[m] = (extract(text))


    return header, data


def extract(text):


    sentence_count = 0 # there is 0 sentence extracted in the beginning
    sentence = ""
    i = 0

    for character in text:

        # if it is an alphabet, we continue counting the word's length
        if character.isalpha():

            sentence = sentence + character

        ### A PROBLEM: HOW DO WE DIFFERENTIATE DECIMALS IN NUMBERS FROM PERIODS? NEED TO IMPLEMENT?
        # if it is a period, that means it is the end of sentence
        #           so we store the length of each words, in the sentence, in sentence token
        elif (character == ".") or (character == "!") or (character == "?"): # newline is not considered another sentence

            ### WATCH   # for handling decimal cases, since "." in decimals arent supposed to be treated as the end of sentence.
            if character == ".":
                if (i - 1) >= 0:  # preventing errors from checking index that does not exist
                    if isinstance(text[i - 1], int):
                        if (i - 1) < len(text):
                            if isinstance(text[i + 1], int):
                                # if it is actually a decimal, it should not be treated as end of sentence,
                                # so we just continue scanning with the text

                                sentence = sentence + character

                                continue


            sentence_count, sentence = increase_sentence_count_if_we_should(sentence, sentence_count, character)

            # if it is not an alphabet, or a period,
        else:

            sentence = sentence + character


        i += 1

        # if we have 10 sentences extracted already, return these 10
        if sentence_count == 10: # 9 cuz we already have 1 sentence in the beginning, and is a
            return sentence

    # for if the text have less than 10 sentences
    increase_sentence_count_if_we_should(sentence, sentence_count, "") # not keeping any output since we dont arent using anymore outputs anyway

    return sentence


def increase_sentence_count_if_we_should(sentence, sentence_count, character):



    # sentence length being 0 means there is no sentence to add
    # because sentences that have no words are not considered a sentence
    if (len(sentence) > 0) and (sentence_count < 10):
        sentence = sentence + character
        sentence_count = sentence_count + 1

    return sentence_count, sentence


if __name__ == "__main__":

    the_dataset_file_name = sys.argv[1]  # line is for taking inputs from cmd, if we are using cmd

    d_header, d_data = main_function(the_dataset_file_name)


    # write our output csv
    output_file_name = "ten_sentences_extracted" + " " + the_dataset_file_name
    # write our new csv, with ARI added as a new last column, as output
    with open(output_file_name, mode='w', newline='', encoding= "utf-8") as writing_file:
        file_writer = csv.writer(writing_file, delimiter=',')

        file_writer.writerow(d_header)
        for row in d_data:
            file_writer.writerow(row)