import unittest
from unittest import TestCase, mock
from module_emoji_processing import emojis_extractor
from module_emoji_processing import replace_emojis_within_text
from module_emoji_processing import convert_multi_char_emoji_to_emoji
from module_emoji_processing import init_emoticon_to_emotion
from module_emoji_processing import convert_multi_char_emoji_to_emotion
from module_emoji_processing import EmojiProcessingNotInitialised
from module_emoji_processing import list_of_emoticons_emotion

init_emoticon_to_emotion()
class Test(unittest.TestCase):

    def test_unit_convertemojitext_to_emojis(self):
        text = ':D'
        result = convert_multi_char_emoji_to_emoji(text)
        self.assertEqual(result, "😁")

    def test_unit_convertemojitext_to_emojis_withpunctuationwrapped_chars(self):
        text = ':D,'
        result = convert_multi_char_emoji_to_emoji(text)
        self.assertEqual(result, "😁")
        text = ',:D'
        result = convert_multi_char_emoji_to_emoji(text)
        self.assertEqual(result, "😁")
        text = 'hello ,:D, there'
        result = convert_multi_char_emoji_to_emoji(text)
        self.assertEqual(result, "hello 😁 there")
        self.assertNotEqual(result, "hello😁there")

    def test_unit_extract_emojis_from_text(self):
        text = '🤤'
        result = replace_emojis_within_text(text)
        self.assertEqual(result, " Happy ")
        text = 'I am so happy 🤤'
        result = replace_emojis_within_text(text)
        self.assertEqual(result, "I am so happy  Happy ")
        text = 'I am so sad 🤐'
        result = replace_emojis_within_text(text)
        self.assertEqual(result, "I am so sad  Sad ")
        text = 'I am so 🤢'
        result = replace_emojis_within_text(text)
        self.assertEqual(result, "I am so  Fear ")

    def test_unit_extract_emojis_from_text_surroundedbypunctuation(self):
        text = 'I am so a🤢 b'
        result = replace_emojis_within_text(text)
        self.assertEqual(result, "I am so Fear b")

    # TODO 
    # this doesn't work yet we eed to iterate down all surround items till it works    
    # def test_unit_extract_emojis_from_text_surroundedbypunctuation(self):
    #     text = 'I am so a🤢 b'
    #     result = replace_emojis_within_text(text)
    #     self.assertEqual(result, "I am so Fear b")

    def test_doesnotexist(self):
        text='blah blah'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, text)

    def test_generate_emoticons_to_emotions(self):
        text=':)'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, " Happy ")
        text='^^'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, " Happy ")
        text='\\o/'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, "")
        text='</3'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, " Sad ")

    def test_unit_handles_embedded_in_strings(self):
        text='My </3 all over again'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, "My  Sad  all over again")
        text='I am so so >_>^'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, "I am so so  Angry ")

    def test_unit_handles_emoticons_but_ignores_emojis(self):
        text='I am happy :-) just so 😛'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, "I am happy  Happy  just so 😛")

    def test_unit_handles_multi(self):
        text='My </3 all over again and very >_>^'
        result = convert_multi_char_emoji_to_emotion(text)
        self.assertEqual(result, "My  Sad  all over again and very  Angry ")

    # note we will likely remove for production so we dont put overhead into code
    @mock.patch('module_emoji_processing.is_list_of_emoticons_emotion_empty',mock.MagicMock(return_value=True))
    def test_unit_handles_not_initialised(self):
        with self.assertRaises(EmojiProcessingNotInitialised) as context:
            convert_multi_char_emoji_to_emotion("Blah")

    def test_unit_handles_punctuation_around_emoticon1(self):
        t = "This is the bomb :-), wow"
        result = convert_multi_char_emoji_to_emotion(t)
        self.assertEqual(result, "This is the bomb  Happy  wow")

    def test_unit_handles_punctuation_around_emoticon2(self):
        t = "This is the bomb ,:-), wow"
        result = convert_multi_char_emoji_to_emotion(t)
        self.assertEqual(result, "This is the bomb  Happy  wow")

    def test_unit_handles_punctuation_around_emoticon_causesindexerror(self):
        t = "This is the bomb ,:, wow"
        result = convert_multi_char_emoji_to_emotion(t)
        self.assertEqual(result, "This is the bomb ,:, wow")
        t = "This is the bomb ,, wow"
        result = convert_multi_char_emoji_to_emotion(t)
        self.assertEqual(result, "This is the bomb ,, wow")


if __name__ == '__main__':
    unittest.main()