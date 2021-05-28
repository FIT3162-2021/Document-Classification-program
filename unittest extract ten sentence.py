import unittest


from extractTenSentence import *


class TestTheMainFunction(unittest.TestCase):

    def test_the_main_non_existent_file(self):
        """
        Test to make sure it throws error as expected with non_existent_file
        """
        with self.assertRaises(SystemExit):
            the_main_function("non existent file")

    def test_the_main_empty_file(self):
        """
        Test to make sure it throws error as expected with empty_file
        """
        with self.assertRaises(SystemExit):
            the_main_function("testfile_empty_file.csv")

    def test_the_main_non_csv_file(self):
        """
        Test to make sure it throws error as expected with non_csv file
        """
        with self.assertRaises(SystemExit):
            the_main_function("test_file_not_a_csv")

    def test_the_main_with_non_utf_file(self):
        """
        Test to make sure it throws error as expected with non-utf8 file
        """
        with self.assertRaises(SystemExit):
            the_main_function('test_non_utf_8.csv.csv')

    def test_the_main_with_simple_yet_proper_file(self):
        """
        Test for it running as expected with proper file
        """
        assert the_main_function('test_proper_file.csv') == (['\ufeffid', 'link'], [['1', 'abc.com'], ['2', 'gef.com']])

    def test_the_main_with_proper_file_two(self):
        """
        Test for it running as expected with proper file two
        """
        assert the_main_function('test_proper_file_2.csv') == (['\ufeffUnique_ID', 'Link', 'Title', 'Text'], [['', 'https://www.timeforkids.com/k1/ready-set-recycle-2/', 'Ready, Set, Recycle!', 'On Earth Day, people all around the world help the planet. But you can help the planet anytime. Recycling is an important way to do this. Do you recycle? Read on to learn more about it.\n\nWhat Can I Recycle?\n\nPaper can be recycled. So can metal, plastic, and glass. Give those a rinse first.\n\nKeep It Separated\n\nPut each material into a different bin.'], ['', 'a', 'c', 'apple is of the color red.']])

    def test_the_main_with_proper_file_three(self):
        """
        Test for it running as expected with proper file three
        """
        assert the_main_function('test_proper_file_3.csv') == (['\ufeffUnique_ID', 'Link', 'Title', 'Text'], [['', 'https://www.timeforkids.com/k1/ready-set-recycle-2/', 'Ready, Set, Recycle!', 'On Earth Day, people all around the world help the planet. But you can help the planet anytime. Recycling is an important way to do this. Do you recycle? Read on to learn more about it.\n\nWhat Can I Recycle?\n\nPaper can be recycled. So can metal, plastic, and glass. Give those a rinse first.\n\nKeep It Separated\n\nPut each material into a different bin.'], ['', 'https://www.timeforkids.com/k1/lets-compost/', "Let's Compost!", 'This Earth Day, why not make a compost bin? Put some soil in a plastic bin or tub. Add leaves and twigs. Moisten with water. Now you can add scraps of fruits and vegetables. You can also add coffee grounds and old tea bags.\n\nHow does composting work? Tiny creatures found in soil will feast on the food scraps. They will break them down. The soil will become rich with nutrients.'], ['', 'https://www.timeforkids.com/k1/be-here-now-2/', 'Be Here Now', 'Mindfulness is taught in many schools. Kids learn deep breathing, movement, and how to relax. Mindfulness can help people in different ways. Read on to learn more.\n\nCalm Down\n\nMindfulness helps people relax. It calms the body. It also quiets the mind.\n\nBe Happy\n\nMindfulness helps people feel good. It reduces anger and sadness. It is said to boost happiness.']])


class TestExtract(unittest.TestCase):

    def test_extract_when_input_is_less_than_ten_sentences(self):
        """
        test for when input is less than ten sentences
        """
        assert (extract('this is a sentence. this too. 3122313 and these as well. four. five. six.')) == 'this is a sentence. this too. 3122313 and these as well. four. five. six.'

    def test_extract_when_input_is_more_than_ten_sentences(self):
        assert (extract('this is a sentence. this too. 3122313 and these as well. four. five. six. seven. eight. nine. ten. eleven. sentences.')) == 'this is a sentence. this too. 3122313 and these as well. four. five. six. seven. eight. nine. ten.'

    def test_extract_when_there_are_newlines(self):
        assert (extract('this is a sentence. this too. 3122313 and these as well. \n\n\n\nfour. five. six. seven. eight. nine. ten. eleven. sentences.')) == 'this is a sentence. this too. 3122313 and these as well. \n\n\n\nfour. five. six. seven. eight. nine. ten.'


class TestIncreaseSentenceCountIfWeShould(unittest.TestCase):

    def test_for_correct_updating_one(self):
        """
        check if it updates correctly when it should
        """
        assert increase_sentence_count_if_we_should('one. two. three.', 3, 'a') == (4, 'one. two. three.a')

    def test_for_correct_updating_two(self):
        """
        check if it doesnt update when it should not.
        """
        assert increase_sentence_count_if_we_should('one. two. three. four.five.six.seven.eight. nine. ten.', 10, 'a') \
               == (10, 'one. two. three. four.five.six.seven.eight. nine. ten.')


if __name__ == '__main__':

    unittest.main()
