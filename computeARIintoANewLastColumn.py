import sys
import csv
import os

# NOTE:
# ***input file must be (.csv), with utf-8 encoding, for the program to run.
#
# ***input file should contain header. because the first row of the csv file will be considered as header.
#
# ***OUR ARI FORMULA IS AS BELOW:
#
#             ari_score = 0.50(w/s) + 4.71(s/w) - 21.43
#             where ari_score = assigned grade level
#             w/s = words per sentence or sentence length,
#             s/w = characters per word or word length.
#             define Python user-defined exceptions


class Error(Exception):
    """Base class for other exceptions"""
    pass


class EmptyFileError(Error):
    """Raised when the the file is empty"""
    pass


class NotCsvFileError(Error):
    """Raised when the the file is not csv, when the functions expects .csv file type"""
    pass


def readfile(dataset_file_name):
    """
    This functions opens the csv file with the input file name, and returns its header and rows.
    :precondition: It expects the file to be opened as a .csv file, with "utf 8" encoding. Must not be an empty file.
    :param dataset_file_name: the .csv dataset's file name
    :complexity: O(m), where m is length of the file.
    :return: two tuple (f_header, f_row)
                WHERE
                list f_header is the list containing header data of the csv

                list f_row is the list containing data of all rows in the csv, excluding the header
    """

    # error handling, checking for empty file or non existent file, and also for .csv file type
    try:

        # test for if it is file exists
        if os.stat(dataset_file_name).st_size > 0:
            print("Reading file...")
        else:
            raise EmptyFileError

        # test for if it is csv file type
        name, extension = os.path.splitext(dataset_file_name)
        if extension\
                == ".csv":
            print("Reading file...")
        else:
            raise NotCsvFileError

        # our program expects only utf-8, so we test for encodings
        test_reader = open(dataset_file_name, "r", encoding='utf-8')
        next(test_reader)    # this is necessary because the error is only thrown when running next()
        test_reader.close()

    except OSError as e:
        raise SystemExit("URL file missing ... exiting".format(e)) from None
    except EmptyFileError as e:
        raise SystemExit("Empty URL file ... exiting".format(e)) from None
    except NotCsvFileError as e:
        raise SystemExit("Expected .csv file, a file that is not .csv has been received ... exiting".format(e)) from \
            None
    except UnicodeDecodeError as e:
        test_reader.close()
        raise SystemExit("File needs to be in utf-8 encoding ... exiting".format(e)) from None

    f_data = []

    # opens our file, assuming our encoding as "utf-8"  ### TEST? NON "utf-8" may throw errors
    with open(dataset_file_name, "r", encoding='utf-8') as csv_file:

        opened_file = csv.reader(csv_file, delimiter=',')

        # set header data for returning
        f_header = next(opened_file)

        for row_values in opened_file:
            f_data.append(row_values)

    print("Finished reading file.")
    return f_header, f_data


def tokenize(text):
    """
    This function takes the text, tokenizes each of its sentence as a sentence token, and stores each words in the
    sentence as a world length in the sentence token.
    :param text: the string text to be tokenized
    :complexity: O(n), where m is length of text.
    :return: list token
            WHERE
                token is a list of sentence_tokens, each sentence in the input text is stored as one sentence_token,
                    each sentence_token stores each of its word as integer word_length
    """

    # test to make sure input is string, function is meant to only work with string input
    try:
        if not isinstance(text, str):
            raise TypeError
    except TypeError as e:
        raise SystemExit("The last row of the file, must be in string format ... exiting".format(e)) from None

    # NOTE: "sentences" that have no words are not considered a "sentence"
    token = []  # the token that will store sentence_tokens is initialised here
    word_length = 0
    sentence_tokens = []  # initialise
    i = 0
    for character in text:

        # if it is an alphabet, we continue counting the word's length
        if character.isalpha():

            word_length += 1

        # if it is a period, that means it is the end of sentence
        #           so we store the length of each words, in the sentence, in sentence_tokens
        elif (character == ".") or (character == "!") or (character == "?") or (character == "\n"):

            if character == ".":
                if (i-1) >= 0:  # preventing errors from checking index that does not exist
                    if text[i-1].isdigit():
                        if (i+1) < len(text):
                            if text[i+1].isdigit():
                                # if it is actually a decimal, it should not be treated as end of sentence,
                                # so we just continue scanning with the text

                                continue

            check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens,
                                                                                            word_length, token)
            word_length = 0
            sentence_tokens = []

        # if it is not an alphabet, or a period,
        else:

            # if there is a word prior to this, add it to the sentence token
            if word_length > 0:
                # that is the end of the word, add its length to sentence_tokens
                sentence_tokens.append(word_length)

                word_length = 0

        i += 1

    # for if the text does not end with a "." or "?" or "!" or "\n", and the sentence has not been added to token yet
    check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length, token)

    return token


def check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens,
                                                                                    word_length, dtoken):
    """
    The functions checks if there is word_length to add to the sentence token, and if there is, add it. It then checks
    for if there is a sentence_token that should be added to our token, if there is, add it
    :param sentence_tokens: the list sentence_token that is meant to hold the word length for all words in the
    sentence it represents
    :param word_length: the integer word_length at the current step of iteration
    :param dtoken: the list token that stores sentence_tokens for the document
    :complexity: O(1)
    :return:
            None
    :postcondition: dtoken gets updated accordingly
    """
    # function does exactly what it name says it does

    # word length being 0 means there is no word to add to the
    # because a word that have no characters is not considered a word
    if word_length > 0:
        sentence_tokens.append(word_length)

    # sentence length being 0 means there is no sentence to add
    # because sentences that have no words are not considered a sentence
    if len(sentence_tokens) > 0:
        dtoken.append(sentence_tokens)

    return


def get_classification(ari_score):
    """
    This function takes the text's ARI score, and returns its classification for the text
    :param ari_score: integer ARI score
    :complexity: O(1)
    :return: integer classification
        where
                # Classification:
                #  If we use every 3 lv is a new lv,:
                # <4:beginner ->stored as integer 1
                # 4~6.9999:intermediate->stored as integer 2
                # 7~9.9999: competent>stored as integer 3
                # 10~12.9999:advanced>stored as integer 4
                # 13+:expert  ->stored as integer 5
    """

    if ari_score < 4:  # if value is between 0 ~ 3.999999999
        return 1
    elif (ari_score >= 4) & (ari_score < 7):  # if value is between 4 ~ 6.999999999
        return 2
    elif (ari_score >= 7) & (ari_score < 10):  # if value is between 7 ~ 9.999999999
        return 3
    elif (ari_score >= 10) & (ari_score < 13):  # if value is between 10 ~ 12.999999999
        return 4
    elif ari_score >= 13:  # if value is 13 or more
        return 5


def calculate_ari_array(tokens):
    """
    This functions takes tokens as input and use it to calculate an array of ARI scores for the data used in creating
    tokens.
    :param tokens: list token
                        WHERE
                            token is a list of sentence_tokens, each sentence in the input text is stored as one
                            sentence_token,
                                each sentence_token stores each of its word as integer word_length
    :complexity: O(r), where r is the number of tokens within tokens
    :return: list ari_array which is containing the ARI score in each index
    """
    ari_array = []  # stores the ARI value, to be appended to the new last column is csv

    for pre_processed_row_data in tokens:
        sum_of_words = 0
        sum_of_characters = 0
        number_of_sentences = len(pre_processed_row_data)

        # each pre_processed_row_data is a token containing the row'text's tokenized data
        for j in pre_processed_row_data:
            sum_of_words += len(j)
            sum_of_characters += sum(j)

        try:
            if (number_of_sentences == 0) or (sum_of_words == 0):
                raise ZeroDivisionError
        except ZeroDivisionError as e:
            raise SystemExit("Cell containing no words detected in csv file's last column, each cell in the last "
                             "column must contain one or more word ... exiting".format(e)) from None

        # calculate ARI score using our formula and append it to ari_array
        x = (0.5 * sum_of_words / number_of_sentences)
        y = (4.71 * sum_of_characters / sum_of_words)
        ari_value = x + y - 21.43
        ari_array.append(ari_value)

    return ari_array


def main_function(dataset_file_name):
    """
    This functions calculates ARI score and classification of the text in csv data, add them as last row, and returns
    the data with the 2 new ARI score and classification score added.
    :precondition: dataset must be .csv
                   the text data must be in the last row for our dataset
    :param dataset_file_name: the .csv dataset's file name
    :complexity: O(m), where m is length of the file.
    :return: tuple (header, data)
                WHERE
                    header is the first header row to be added to our output csv in list format

                    data is the rows to be added to our output csv in list format, and each row in data
                    represents a document
    """

    # read our csv file
    header, data = readfile(dataset_file_name)

    print("Processing ...")

    # m is the index of the last cell of in a row
    # we assume all row are has the same number of columns in the CSV
    m = len(data[0]) - 1

    # note that each row is assumed to represent a document
    # for each document, tokenize its text
    tokens = []
    for cur_row in data:
        text = cur_row[m]
        tokens.append(tokenize(text))

    # calculate an array of ari_scores using tokens
    d_ari_array = calculate_ari_array(tokens)

    # add ARI column to a new column in our data
    i = 0
    for cur_row in data:
        cur_row.append(d_ari_array[i])
        i += 1

    # update header for our data
    header.append("ARI")

    # add classification column to a new column in our data
    i = 0
    for cur_row in data:
        classification = get_classification(d_ari_array[i])
        cur_row.append(classification)
        i += 1

    # update header for our data
    header.append("Classification")

    print("Finished processing")
    return header, data


if __name__ == "__main__":

    the_dataset_file_name = sys.argv[1]  # line is for taking inputs from cmd, if we are using cmd

    # # if u are not using cmd, comment the cmd line right above this and uncomment the line right below
    # # and input ur file name(.csv) below.
    # the_dataset_file_name = "test_non_utf_8.csv"

    # calculates ARI score and classification of the text in csv data, and return the data in the csv dataset with
    # 2 new last rows, which is a new last row for ari_score, followed by a new row for classification
    d_header, d_data = main_function(the_dataset_file_name)

    # write our output csv
    output_file_name = "csv_output" + " " + the_dataset_file_name
    # write our new csv, with ARI added as a new last column, as output
    with open(output_file_name, mode='w', newline='', encoding="utf-8") as writing_file:
        file_writer = csv.writer(writing_file, delimiter=',')

        file_writer.writerow(d_header)
        for row in d_data:
            file_writer.writerow(row)
