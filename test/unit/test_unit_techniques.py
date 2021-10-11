import unittest

# from module_preprocesstweet import *
from techniques import *
from module_commontextcleaning import *


class Test(unittest.TestCase):

    def test_removeUnicode(self):
        text = "hello \u002c there"
        result = removeUnicode(text)
        self.assertEqual(result, "hello , there")

    def test_replaceURL(self):
        text = "hello http://www.bbc.com there"
        result = replaceURL(text)
        self.assertEqual(result, "hello url there")
        text = "Goodbye http://www.bbc.com there"
        result = replaceURL(text)
        self.assertEqual(result, "Goodbye url there")

    def test_replaceAtUser(self):
        text = "hello @Hellothere there"
        result = replaceAtUser(text)
        self.assertEqual(result, "hello atUser there")

    def test_removeHashtagInFrontOfWord(self):
        text = "hello #hastag there"
        result = removeHashtagInFrontOfWord(text)
        self.assertEqual(result, "hello hastag there")

    def test_removeNumbers(self):
        text = "hello xxx there"
        result = removeNumbers(text)
        self.assertEqual(result, "hello xxx there")


    def test_replaceMultiExclamationMark(self):
        text = "hello !!! there"
        result = replaceMultiExclamationMark(text)
        self.assertEqual(result, "hello  multiExclamation  there")

    def test_replaceMultiQuestionMark(self):
        text = "hello ??? there"
        result = replaceMultiQuestionMark(text)
        self.assertEqual(result, "hello  multiQuestion  there")
        text = "hello ??? there ???"
        result = replaceMultiQuestionMark(text)
        self.assertEqual(result, "hello  multiQuestion  there  multiQuestion ")

    def test_replaceMultiStopMark(self):
        text = "hello ... there"
        result = replaceMultiStopMark(text)
        self.assertEqual(result, "hello  multiStop  there")

    def test_countMultiExclamationMarks(self):
        text = "hello !!! there"
        result = countMultiExclamationMarks(text)
        self.assertEqual(result, 1)
        text = "!!!hello !!! there!!!"
        result = countMultiExclamationMarks(text)
        self.assertEqual(result, 3)

    def test_countMultiQuestionMarks(self):
        text = "hello ??? there ???"
        result = countMultiQuestionMarks(text)
        self.assertEqual(result, 2)

    def test_countMultiStopMarks(self):
        text = "..hello ... there...."
        result = countMultiStopMarks(text)
        self.assertEqual(result, 3)

    # dont know what this is so what do we need to test ;-)
    def test_countElongated(self):
        text = "hello"
        result = countElongated(text)
        self.assertEqual(result, 0)
        text = "hellooooo"
        result = countElongated(text)
        self.assertEqual(result, 1)

    def test_countAllCaps(self):
        text = "HELLO how ARE you"
        result = countAllCaps(text)
        self.assertEqual(result, 2)

    def test_countSlang(self):
        text = "b4n bravo"
        result = countSlang(text)
        self.assertEqual(result,  (2, ['b4n', 'bravo']))

    def test_replaceContraction(self):
        text = "hello dammit"
        result = replaceContraction(text)
        self.assertEqual(result, "hello damn it")

    def test_replaceElongated(self):
        text = "helloooo there"
        result = replaceElongated(text)
        self.assertEqual(result, "helo there")

    def test_removeEmoticons(self):
        text = "hello:-) there"
        result = removeEmoticons(text)
        self.assertEqual(result, "hello there")

    def test_countEmoticons(self):
        text = "hello :-) ;) there"
        result = countEmoticons(text)
        self.assertEqual(result, 2)

    def test_words(self):
        text = "hello   there how are you"
        result = words(text)
        self.assertEqual(result, ['hello', 'there', 'how', 'are', 'you'])
        text = ""
        result = words(text)
        self.assertEqual(result, [])
        text = "hello"
        result = words(text)
        self.assertEqual(result, ['hello'])

    def test_P(self):
        text = "twentieth"
        result = P(text)
        self.assertEqual(result, 1.7031422975389594e-05)
        text = "hello there"
        result = P(text)
        self.assertEqual(result, 0.0)
        text = "hello"
        result = P(text)
        self.assertEqual(result, 8.963906829152417e-07)

    def test_addNotTag(self) :
        text = "hello not there however."
        result = addNotTag(text)
        self.assertEqual(result, "hello not NEG_there NEG_however.")

    def test_addCapTag(self) :
        text = "HELLO"
        result = addCapTag(text)
        self.assertEqual(result, "ALL_CAPS_HELLO")
        text = "HELLO THERE"
        result = addCapTag(text)
        self.assertEqual(result, "ALL_CAPS_HELLO THERE ALL_CAPS_HELLO THERE")
        # self.assertEqual(result, "there is ALL_CAPS_there is HELLO there how ARE you there how ALL_CAPS_there is HELLO there how ARE you you")

# def countEmoticons(text):
# def words(text): return re.findall(r'\w+', text.lower())
# def P(word, N=sum(WORDS.values())): 
# def spellCorrection(word): 
# def candidates(word): 
# def known(words): 
# def edits1(word):
#     letters    = 'abcdefghijklmnopqrstuvwxyz'
# def edits2(word): 
# def replace(word, pos=None):
# def replaceNegations(text):
# def addNotTag(text):
# def addCapTag(word):

if __name__ == '__main__':
    unittest.main()