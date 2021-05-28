import unittest

from computeARIintoANewLastColumn import *


class TestReadFile(unittest.TestCase):
    def test_non_existent_file(self):
        """
        Test the function with non_existent_file
        """
        with self.assertRaises(SystemExit):
            readfile("non existent file")

    def test_empty_file(self):
        """
        Test the function with empty_file
        """
        with self.assertRaises(SystemExit):
            readfile("testfile_empty_file.csv")

    def test_non_csv_file(self):
        """
        Test the function with non_csv file
        """
        with self.assertRaises(SystemExit):
            readfile("test_file_not_a_csv")

    def test_not_utf8_csv_file(self):
        """
        Test the function with not utf8_csv_file type
        """
        with self.assertRaises(SystemExit):
            readfile("test_non_utf_8.csv")

    def test_proper_file(self):
        """
        Test the function with not utf8_csv_file type
        """
        x = (["\ufeffid", 'link'], [['1', 'abc.com'], ['2', 'gef.com']])
        assert readfile("test_proper_file.csv") == x


class TestTokenize(unittest.TestCase):

    def test_tokenize_incorrect_input_type(self):
        """
        Test the function with incorrect input type
        """
        with self.assertRaises(SystemExit):
            tokenize(111)

    def test_tokenize_empty_string(self):
        """
        test if function runs as expected on empty string
        """
        assert tokenize("") == []

    def test_tokenize_numbers_only_string(self):
        """
        test if function runs as expected on a numbers-only string
        """
        assert tokenize("111") == []

    def test_tokenize_special_symbols_only_string(self):
        """
        test if function runs as expected on a special-symbol-only string
        """
        assert tokenize("...") == []

    def test_tokenize_single_word(self):
        """
        test if function runs as expected on a single word string
        """
        assert tokenize("chocolate") == [[9]]

    def test_tokenize_single_sentence(self):
        """
        test if function runs as expected on single sentence string
        """
        assert tokenize("chocolates are the best") == [[10, 3, 3, 4]]

    def test_tokenize_special_case_one(self):
        """
        test for if the function handles decimals within sentences properly
        """
        assert tokenize("apple///..... is the best...a...really.....") == [[5], [2, 3, 4], [1], [6]]

    def test_tokenize_special_case_two(self):
        """
        test if function runs as expected when there is a digit between words in a sentence
        """
        assert tokenize("..ready2eat..") == [[5, 3]]

    def test_tokenize_special_case_three(self):
        """
        test if function runs as expected when sentence ends in digit
        """
        assert tokenize("..ready2.eat.3.") == [[5], [3]]

    def test_tokenize_proper(self):
        """
        test if function runs as expected on normal proper input
        """
        assert tokenize("I love fried chicken \n Fried chicken is the best! Truly!? Lol") == [[1, 4, 5, 7],
                                                                                              [5, 7, 2, 3, 4], [5], [3]]


class TestCheckIfThereIsAnythingToAddIfThereIsThenAddSentenceTokenToDtoken(unittest.TestCase):
    def test_check_one(self):
        """
        test on normal input
        """
        sentence_tokens = [1, 3, 2]
        word_length = 13
        dtoken = ['dummy data']
        check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length,
                                                                                        dtoken)

        assert dtoken == ['dummy data', [1, 3, 2, 13]]

    def test_check_two(self):
        """
        test on normal input, with empty sentence_tokens
        """
        sentence_tokens = []
        word_length = 13
        dtoken = ['dummy data']
        check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length,
                                                                                        dtoken)

        assert dtoken == ['dummy data', [13]]

    def test_check_three(self):
        """
        test on normal input, with empty sentence_tokens and dtoken
        """
        sentence_tokens = []
        word_length = 13
        dtoken = []
        check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length,
                                                                                        dtoken)

        assert dtoken == [[13]]

    def test_check_four(self):
        """
        test on normal input, with empty sentence token and dtoken being list of integers
        """
        sentence_tokens = []
        word_length = 13
        dtoken = [0, 1, 2, 3, 4]
        check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length,
                                                                                        dtoken)

        assert dtoken == [0, 1, 2, 3, 4, [13]]

    def test_check_five(self):
        """
        test on normal input, with empty sentence token and dtoken being list of list
        """
        sentence_tokens = []
        word_length = 13
        dtoken = [['asd'], [1, 3, 66, 6]]
        check_if_there_is_anything_to_add_if_there_is_then_add_sentence_token_to_dtoken(sentence_tokens, word_length,
                                                                                        dtoken)

        assert dtoken == [['asd'], [1, 3, 66, 6], [13]]


class TestGetClassification(unittest.TestCase):

    def test_classification_one(self):
        """
        test classifying for category 1 is working
        """
        assert get_classification(2.123) == 1

    def test_classification_two(self):
        """
        test classifying for category 2 is working
        """
        assert get_classification(5.123) == 2

    def test_classification_three(self):
        """
        test classifying for category 3 is working
        """
        assert get_classification(8.123) == 3

    def test_classification_four(self):
        """
        test classifying for category 4 is working
        """
        assert get_classification(11.123) == 4

    def test_classification_five(self):
        """
        test classifying for category 5 is working
        """
        assert get_classification(14.123) == 5


class TestCalculateARIArray(unittest.TestCase):

    def test_calculate_ari_array_simple_value(self):
        """
        test for one sentence, 1 document token input
        :return:
        """
        assert calculate_ari_array([[[5, 5, 5]]]) == [3.620000000000001]

    def test_calculate_ari_array_one(self):
        """
        first test for two sentence, 1 document token input
        """
        assert calculate_ari_array([[[11, 8], [9, 9, 1, 3, 5]]]) == [11.271428571428572]

    def test_calculate_ari_array_two(self):
        """
        second test for four sentence, 1 document token input
        """
        assert calculate_ari_array([[[5], [2, 10, 13], [1], [6]]]) == [8.365000000000002]

    def test_calculate_ari_array_three(self):
        """
        test for token input containing 2 documents
        """
        assert calculate_ari_array([[[11, 8], [9, 9, 1, 3, 5]], [[5], [2, 10, 13], [1], [6]]]) == [11.271428571428572,
                                                                                                   8.365000000000002]

    def test_calculate_ari_array_four(self):
        """
        test for token input containing 3 documents
        """
        assert calculate_ari_array([[[11, 8], [9, 9, 1, 3, 5]], [[5], [2, 10, 13], [1], [6]],
                                    [[5, 5, 5]]]) == [11.271428571428572, 8.365000000000002, 3.620000000000001]


class TestMainFunction(unittest.TestCase):
    def test_main_non_existent_file(self):
        """
        Test to make sure it throws error as expected with non_existent_file
        """
        with self.assertRaises(SystemExit):
            main_function("non existent file")

    def test_main_empty_file(self):
        """
        Test to make sure it throws error as expected with empty_file
        """
        with self.assertRaises(SystemExit):
            main_function("testfile_empty_file.csv")

    def test_main_non_csv_file(self):
        """
        Test to make sure it throws error as expected with non_csv file
        """
        with self.assertRaises(SystemExit):
            main_function("test_file_not_a_csv")

    def test_main_with_non_utf_file(self):
        """
        Test to make sure it throws error as expected with non-utf8 file
        """
        with self.assertRaises(SystemExit):
            main_function('test_non_utf_8.csv.csv')

    def test_main_with_file_with_cell_in_last_column_without_words(self):
        """
        Test to make sure it throws error as expected when a last column in the .csv file, contains one or more cell
        with no words
        """
        with self.assertRaises(SystemExit):
            main_function('test_file_one_last_column_cell_has_no_words.csv')

    def test_main_with_simple_yet_proper_file(self):
        """
        Test for it running as expected with proper file
        """
        assert main_function('test_proper_file.csv') == (['\ufeffid', 'link', 'ARI', 'Classification'],
                                                         [['1', 'abc.com', -6.800000000000001, 1],
                                                          ['2', 'gef.com', -6.800000000000001, 1]])

    def test_main_with_proper_file_two(self):
        """
        Test for it running as expected with proper file two
        """
        assert main_function('test_proper_file_2.csv') == (['\ufeffUnique_ID', 'Link', 'Title', 'Text', 'ARI', 'Classification'], [['', 'https://www.timeforkids.com/k1/ready-set-recycle-2/', 'Ready, Set, Recycle!', "On Earth Day, people all around the world help the planet. But you can help the planet anytime. Recycling is an important way to do this. Do you recycle? Read on to learn more about it.\n\nWhat Can I Recycle?\n\nPaper can be recycled. So can metal, plastic, and glass. Give those a rinse first.\n\nKeep It Separated\n\nPut each material into a different bin. This will help recycling centers sort it all out later on.\n\nHere Comes the Truck\n\nA recycling truck will come to take your materials away. Now they're headed to a recycling center.\n\nSorted Out\n\nThe materials will be sorted. They might be compressed, or crushed. They are on their way to becoming something new.\n\nTry It!\n\nUse items in a new way without recycling them. Try making a plastic bottle into an instrument. Plant seeds in an old egg carton.", 1.777543180464562, 1], ['', 'a', 'c', 'apple is of the color red.', -2.729999999999997, 1]])

    def test_main_with_proper_file_three(self):
        """
        Test for it running as expected with proper file three
        """
        assert main_function('test_proper_file_3.csv') == (['\ufeffUnique_ID', 'Link', 'Title', 'Text', 'ARI', 'Classification'], [['', 'https://www.timeforkids.com/k1/ready-set-recycle-2/', 'Ready, Set, Recycle!', "On Earth Day, people all around the world help the planet. But you can help the planet anytime. Recycling is an important way to do this. Do you recycle? Read on to learn more about it.\n\nWhat Can I Recycle?\n\nPaper can be recycled. So can metal, plastic, and glass. Give those a rinse first.\n\nKeep It Separated\n\nPut each material into a different bin. This will help recycling centers sort it all out later on.\n\nHere Comes the Truck\n\nA recycling truck will come to take your materials away. Now they're headed to a recycling center.\n\nSorted Out\n\nThe materials will be sorted. They might be compressed, or crushed. They are on their way to becoming something new.\n\nTry It!\n\nUse items in a new way without recycling them. Try making a plastic bottle into an instrument. Plant seeds in an old egg carton.", 1.777543180464562, 1], ['', 'https://www.timeforkids.com/k1/lets-compost/', "Let's Compost!", 'This Earth Day, why not make a compost bin? Put some soil in a plastic bin or tub. Add leaves and twigs. Moisten with water. Now you can add scraps of fruits and vegetables. You can also add coffee grounds and old tea bags.\n\nHow does composting work? Tiny creatures found in soil will feast on the food scraps. They will break them down. The soil will become rich with nutrients. It can be used to grow plants.\n\nLook at the illustration below. It shows which items should be composted and which should not. Use it to help you with your compost project.', 2.048862690707349, 1], ['', 'https://www.timeforkids.com/k1/be-here-now-2/', 'Be Here Now', "Mindfulness is taught in many schools. Kids learn deep breathing, movement, and how to relax. Mindfulness can help people in different ways. Read on to learn more.\n\nCalm Down\n\nMindfulness helps people relax. It calms the body. It also quiets the mind.\n\nBe Happy\n\nMindfulness helps people feel good. It reduces anger and sadness. It is said to boost happiness.\n\nStay Focused\n\nMindfulness helps people pay attention. It can help kids do well in school.\n\nConnect with Others\n\nMindfulness helps people get along. It increases feelings of empathy. Empathy is the ability to understand and share other people's feelings.\n\nDid You Know?\nYou can practice mindfulness.\n\nHere is one way. Try it.\n\n1) Sit down. Close your eyes.\n\n2) Count to four as you breathe in.\n\n3) Count to four as you breathe out.\n\n4) Repeat three times.", 2.925825396825399, 1]])


if __name__ == '__main__':
    unittest.main()
