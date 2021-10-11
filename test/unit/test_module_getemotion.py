import unittest
from unittest import TestCase, mock
from module_text2emotion import get_emotion
from module_emoji_processing import init_emoticon_to_emotion

class Test(unittest.TestCase):
    def setUp(self):
        init_emoticon_to_emotion()

    def test_emotion_happy(self):
        t = "I am so happy"
        r=get_emotion(t)
        self.assertEqual(r, {'Happy': 1.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 0.0, 'Fear': 0.0})
    
    def test_emotion_angry(self):
        t = "I am so angry"
        r=get_emotion(t)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 1.0, 'Surprise': 0.0, 'Sad': 0.0, 'Fear': 0.0})

    def test_emotion_surprise(self):
        t = "I am so surprised"
        r=get_emotion(t)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 1.0, 'Sad': 0.0, 'Fear': 0.0})

    def test_emotion_sad(self):
        t = "I am so sad"
        r=get_emotion(t)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 1.0, 'Fear': 0.0})

    # doesnt work!
    # def test_emotion_sad_emoji(self):
    #     t = "i feel 🙁"
    #     r=get_emotion(t)
    #     self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 1.0, 'Fear': 0.0})

    def test_emotion_fear(self):
        t = "I am so fearful"
        r=get_emotion(t)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 0.0, 'Fear': 1.0})

    def test_emotion_mixed(self):
        t = "I am so fearful and sad"
        r=get_emotion(t)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 0.5, 'Fear': 0.5})

    def test_emotion_null(self):
        t = "this is neutral"
        r=get_emotion(t)
        self.assertEqual(r, ({'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 0.0, 'Fear': 0.0}, None))

    def test_emotion_emptystring(self):
        t = ""
        r=get_emotion(t)
        self.assertEqual(r, ({'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 0.0, 'Fear': 0.0}, []))

    def test_emotion_returned_cleanedstring(self):
        t = "I am so fearful and sad"
        r,c=get_emotion(t, already_cleaned=False, return_interim_cleaned=True)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 0.0, 'Sad': 0.5, 'Fear': 0.5})
        self.assertEqual(c, ['i', 'am', 'so', 'fearful', 'and', 'sad'])
        self.assertNotEqual(c, ['i', 'am'])

    def test_emotion_returned_cleanedstring_complex(self):
        t = "This is the bomb :-) my god could it be better 😜 i'm so !!!!! pumped!!! 🌺 THANKYOU THANKYOU"
        r,c=get_emotion(t, already_cleaned=False, return_interim_cleaned=True)
        self.assertEqual(r, {'Happy': 0.0, 'Angry': 0.0, 'Surprise': 1.0, 'Sad': 0.0, 'Fear': 0.0})
        self.assertEqual(c, ['this', 'is', 'the', 'bomb', 'Happy', 'my', 'god', 'could', 'it', 'be', 'better', 'Happy', 'i', 'am', 'so', 'multiExclamation', 'pumped', 'multiExclamation', 'Happy', 'thankyou', 'thankyou'])
        self.assertNotEqual(c, ['blah'])

if __name__ == '__main__':
    unittest.main()