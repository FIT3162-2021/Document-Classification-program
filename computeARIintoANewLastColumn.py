import sys
import csv

# TODO:
#       document code properly, and also testing
#           remember to document each class and function, with complexity, input, return, etc
#           (btw need ot double check if preconditions are documented correctly)
#           error handling//catching, such as try and except
### the use of "###" in comments indicates the comment is means as a NOTE, or a possible place to TEST, or A PROBLEM
### THAT NEEDS ADDRESSING

###### BTW, are we better off using regular expression? it is way more efficient to code now that i realize it. as for run time with regex, its probably the same

###### BTW, do we need to explain what the ARI scores actually are in documentation, and also what the classification from the ARI scores mean?

### NOTE: OUR FORMULA FOR ARI SCORE IS DIFFERENT FROM THE ONE IN WIKIPEDIA(AND POTENTIALLY SOME OTHER SOURCES):
# OUR FORMULA IS AS BELOW
# GL = 0.50(w/s) + 4.71(s/w) - 21.43
# where GL = assigned grade level
# w/s = words per sentence or sentence length,
# s/w = characters per word or word length.



def readfile(dataset_file_name):
    """
    This functions opens the csv file with the input file name, and returns its header and rows.
    :precondition: It expects the file to be opened as a .csv file, with "utf 8" encoding.
    :param dataset_file_name: the .csv dataset's file name
    :return: two tuple (f_header, f_row)
                WHERE
                list f_header is the list containing header data of the csv

                list f_row is the list containing data of all rows in the csv, excluding the header
    """
    f_data = []

    # opens our file, assuming our encoding as "utf-8"  ### TEST? NON "utf-8" may throw errors
    with open(dataset_file_name, "r", encoding='utf-8') as csv_file:

        opened_file = csv.reader(csv_file, delimiter=',')

        # set header data for returning
        f_header = next(opened_file)

        for row in opened_file:
            f_data.append(row)

    return f_header, f_data


def tokenize(text):
    """
    This function takes the text, tokenizes each of its sentence as a sentence token, and stores each words in the
    sentence as a world length in the sentence token.
    :param text: the string text to be tokenized
    :return: list token
            WHERE
                token is a list of sentence_tokens, each sentence in the input text is stored as one sentence_token,
                    each sentence_token stores each of its word as integer word_length
    """


    ### NOTE: "sentences" that have no words are not considered a "sentence"
    token = []  # the token that will store sentence_tokens is initialised here
    word_length = 0
    sentence_tokens = []  # initialise
    i = 0
    for character in text:

        # if it is an alphabet, we continue counting the word's length
        if character.isalpha():

            word_length += 1

### A PROBLEM: HOW DO WE DIFFERENTIATE DECIMALS IN NUMBERS FROM PERIODS? NEED TO IMPLEMENT?
        # if it is a period, that means it is the end of sentence
        #           so we store the length of each words, in the sentence, in senttoken
        elif (character == ".") or (character == "!") or (character == "?") or (character == "\n"):

### WATCH   # for handling decimal cases, since "." in decimals arent supposed to be treated as the end of sentence.
            if character == ".":
                if (i-1) >= 0: # preventing errors from checking index that does not exist
                    if isinstance(text[i-1], int):
                        if (i-1) < len(text):
                            if isinstance(text[i+1], int):
                                # if it is actually a decimal, it should not be treated as end of sentence,
                                # so we just continue scanning with the text

                                continue

            check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length, token)
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


def check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length, dtoken):
    """
    The functions checks if there is word_length to add to the sentence token, and if there is, add it. It then checks
    for if there is a sentence_token that should be added to our token, if there is, add it
    :param sentence_tokens: the list sentence_token that is meant to hold the word length for all words in the
    sentence it represents
    :param word_length: the integer word_length at the current step of iteration
    :param dtoken: the list token that stores sentence_tokens for the document
    :return:
            None
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


def get_classification(ARI_score):
    """
    This function takes the text's ARI score, and returns its classification for the text
    :param ARI_score: integer ARI score
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

    if ARI_score < 4: # if value is between 0 ~ 3.999999999
        return 1
    elif (ARI_score >= 4) & (ARI_score < 7): # if value is between 4 ~ 6.999999999
        return 2
    elif (ARI_score >= 7) & (ARI_score < 10): # if value is between 7 ~ 9.999999999
        return 3
    elif (ARI_score >= 10) & (ARI_score < 13): # if value is between 10 ~ 12.999999999
        return 4
    elif ARI_score >= 13: # if value is 13 or more
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
    :return: list ARI_array which is containing the ARI score in each index
    """
    ARI_array = []  # stores the ARI value, to be appended to the new last column is csv

    #########debugging, for if there is a row without words, print the row
    index = 0
    #########debugging, if there is a row without words, print the row

    for pre_processed_row_data in tokens:
        sum_of_words = 0
        sum_of_characters = 0
        number_of_sentences = len(pre_processed_row_data)

        # each pre_processed_row_data is a token containing the row'text's tokenized data
        for j in pre_processed_row_data:
            sum_of_words += len(j)
            sum_of_characters += sum(j)

        #########debugging, if there is a row without words, print the row
        if number_of_sentences == 0:
            print(index)
        if sum_of_words == 0:
            print(index)
        if sum_of_characters == 0:
            print(index)
        #########debugging, if there is a row without words, print the row

        # calculate ARI score using our formula and append it to ARI_array
        x = (0.5 * sum_of_words / number_of_sentences)
        y = (4.71 * sum_of_characters / sum_of_words)
        ARI_value = x + y - 21.43
        ARI_array.append(ARI_value)

        index += 1

    return ARI_array


def main_function(dataset_file_name):
    """
    This functions calculates ARI score and classification of the text in csv data, add them as last row, and returns
    the data with the 2 new ARI score and classification score added.
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
    tokens = []
    for row in data:
        text = row[m]
        tokens.append(tokenize(text))

    print(data[0][m]) ### currently in use for debugging, delete it once its no longer needed
    print(tokens[0]) ### currently in use for debugging, delete it once its no longer needed

    # calculate an array of ARI_scores using tokens
    d_ARI_array = calculate_ari_array(tokens)

    print(d_ARI_array) ### currently in use for debugging, delete it once its no longer needed
    print(max(d_ARI_array)) ### currently in use for debugging, delete it once its no longer needed

    # add ARI column to a new column in our data
    i = 0
    for row in data:
        row.append(d_ARI_array[i])
        i += 1

    # update header for our data
    header.append("ARI")


    # add classification column to a new column in our data
    i = 0
    for row in data:
        classification = get_classification(d_ARI_array[i])
        row.append(classification)
        i += 1

    # update header for our data
    header.append("Classification")

    return header, data


if __name__ == "__main__":

    ### NOTE: we assume the file to be in (.csv) format, and it should also be in "utf-8" encoding   ###TEST we may want to test it is csv, if not, throw exception
    #           * the last row of our csv file must store our text data     ###TEST? may want to throw exception is the input csv does not follow have the text data as law row?
    #           * input csv should contain a header, or else, the first row of the data will be read as header and wont be included in the processing

    # dataset_file_name = sys.argv[1]  #line is for taking inputs from cmd, if we are using cmd
    the_dataset_file_name = "dataset WH.csv"


    # calculates ARI score and classification of the text in csv data, and return the data in the csv dataset with
    # 2 new last rows, which is a new last row for ARI_score, followed by a new row for classification
    d_header, d_data = main_function(the_dataset_file_name)

    # write our output csv
    output_file_name = "csv_output" + " " + the_dataset_file_name
    # write our new csv, with ARI added as a new last column, as output
    with open(output_file_name, mode='w', newline='', encoding= "utf-8") as writing_file:
        file_writer = csv.writer(writing_file, delimiter=',')

        file_writer.writerow(d_header)
        for row in d_data:
            file_writer.writerow(row)


