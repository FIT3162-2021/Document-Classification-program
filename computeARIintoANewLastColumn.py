import sys
import csv

# TODO:
#       document code properly, and also testing
#           remember to document each class and function, with complexity, input, return, etc
#           (btw need ot double check if preconditions are documented correctly)
### indicates the comment is means as a NOTE, or a possible place to TEST, or A PROBLEM THAT NEEDS ADDRESSING

###### BTW, are we better off using regular expression? it is way more efficient to code now that i realize it. as for run time with regex, its probably the same

def readfile(dataset_file_name):
    """
    This functions opens the csv file with the input file name, and returns its header and rows.
    :precondition: It expects the file to be opened as a csv file, with "utf 8" encoding.
    :param dataset_file_name: the .csv dataset's file name
    :return: two tuple (f_header, f_row)
        WHERE
        list f_header is the list containing header data of the csv
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

    :param text:
    :return:
    """
    # what this functions does is,
    #       it returns @token
    #           @token, is a list, in each index, it stores all @word_lengths_in_sentence
    #                   @word_lengths_in_sentence is a list: in each index is @word_length, each index represents a word
    #                           @word_length is (interger) length of the word the index represents in @word_lengths_in_sentence

    ### NOTE: "sentences" that have no words are not considered a "sentence"
    # TODO: tokenize
    token = []  # it will store row in each index
    word_length = 0
    sentence_tokens = []  # initialise
    for character in text:

        # if it is an alphabet, we continue counting the word's length
        if character.isalpha():


            word_length += 1

### A PROBLEM: HOW DO WE DIFFERENTIATE DECIMALS IN NUMBERS FROM PERIODS? NEED TO IMPLEMENT?
        # if it is a period, that means it is the end of sentence
        #           so we store the length of each words, in the sentence, in token
        elif (character == ".") or (character == "!") or (character == "?") or (character == "\n"):


            # "sentences" that have no words are not considered a "sentence"
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

    # for if the text does not end with a "." or "?" or "!" or "\n", and the sentence has not been added to token yet
    check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length, token)

    return token


def check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length, dtoken):
    # function does exactly what it name says it does

    if word_length > 0:
        sentence_tokens.append(word_length)
    if len(sentence_tokens) > 0:
            dtoken.append(sentence_tokens)

    return


def getclassification(ARI_score):

# Classification:
#  If we use every 3 lv is a new lv,:
# <3:beginner ->stored as integer 1
# 4~6:intermediate->stored as integer 2
# 7~9: competent>stored as integer 3
# 10~12:advanced>stored as integer 4
# 12+:expert  ->stored as integer 5
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

if __name__ == "__main__":

    ### NOTE: we assume the file to be in (.csv) format, and it should also be in "utf-8" encoding   ###TEST we may want to test it is csv, if not, throw exception
    #           * the last row of our csv file must store our text data     ###TEST? may want to throw exception is the input csv does not follow have the text data as law row?
    #           * input csv should contain a header, or else, the first row of the data will be read as header and wont be included in the processing

    # dataset_file_name = sys.argv[1]  #line is for taking inputs from cmd, if we are using cmd
    dataset_file_name = "dataset-food reviews(Mayesha).csv"

    # read our csv file
    header, data = readfile(dataset_file_name)

    # m is the index of the last cell of in a row
    # we assume all row are has the same number of columns in the CSV
    m = len(data[0]) - 1

    # TODO: TOKENIZE
    tokens = []
    for row in data:
        text = row[m]


        tokens.append(tokenize(text))

    print(data[0][m])
    print(tokens[0])

    # TODO:
    #       calculate ARI from these tokenized data

    ARI_array = [] # stores the ARI value, to be appended to the new last column is csv


#########debugging, for if there is a row without words, print the row
    index = 0
#########debugging, if there is a row without words, print the row
    for pre_processed_row_data in tokens:
        sum_of_words = 0
        sum_of_characters = 0
        number_of_sentences = len(pre_processed_row_data)
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

        x = (0.5 * sum_of_words / number_of_sentences)
        y = (4.71 * sum_of_characters / sum_of_words)
        ARI_value = x + y - 21.43
        ARI_array.append(ARI_value)

        index += 1

    print(ARI_array)
    print(max(ARI_array))
    # TODO: append ARI array to the last column in csv

    # add ARI column to a new column in our data
    i = 0
    for row in data:
        row.append(ARI_array[i])
        i += 1

    #update header for our data
    header.append("ARI")

#Classification:
#  If we use every 3 lv is a new lv,:
# <3:beginner ->stored as integer 1
# 4~6:intermediate->stored as integer 2
# 7~9: competent>stored as integer 3
# 10~12:advanced>stored as integer 4
# 12+:expert  ->stored as integer 5

    # add classification column to a new column in our data
    i = 0
    for row in data:
        classification = getclassification(ARI_array[i])
        row.append(classification)
        i += 1

    #update header for our data
    header.append("Classification")


    output_file_name = "csv_output" + " " + dataset_file_name
    # write our new csv, with ARI added as a new last column, as output
    with open(output_file_name, mode='w', newline='', encoding= "utf-8") as writing_file:
        file_writer = csv.writer(writing_file, delimiter=',')

        file_writer.writerow(header)
        for row in data:
            file_writer.writerow(row)



    #
    # i = 0
    # for k in data:
    #     print(i, k)
    #     i += 1
    #
    # print(header)
