import re
import os
from functools import partial
from module_emoji_processing import *

thisfilelocation = os.path.dirname(os.path.abspath(__file__))


regex_replaceUnicode_match1 = re.compile(r'(\\u[0-9A-Fa-f]+)')
regex_replaceUnicode_match2 = re.compile(r'[^\x00-\x7f]')
# regex_replaceURL_match1= re.compile('((www\.[^\s]+)|(https?://[^\s]+))')
# regex_replaceURL_match2= re.compile('#([^\s]+)')
regex_replaceURL_match1= re.compile('((www\.[^\s]+)|(https?://[^\s]+))')
regex_replaceURL_match2= re.compile('#([^\s]+)')
regex_replaceAtUser = re.compile('@[^\s]+')
regex_removeHashtagInFrontOfWord = re.compile(r'#([^\s]+)')
regex_replaceMultiExclamationMark = re.compile(r"(\!)\1+")
regex_replaceMultiQuestionMark = re.compile(r"(\?)\1+")
regex_replaceMultiStopMark = re.compile(r"(\.)\1+")
# regex_countMultiExclamationMarks = re.compile(r"(\!)\1+")
# regex_countMultiQuestionMarks = re.compile(r"(\?)\1+")
# regex_countMultiStopMarks = re.compile(r"(\.)\1+")
# regex_countElongated = re.compile(r"(.)\1{2}")
# regex_countAllCaps = re.compile("[A-Z0-9]{3,}")
regex_removeEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
# regex_removeEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
# regex_countEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
regex_words = re.compile(r'\w+') 
# regex_addNotTag1 = re.compile(r'\b(?:not|never|no)\b[\w\s]+[^\w\s]', flags=re.IGNORECASE)
# regex_addNotTag2 = re.compile(r'(\s+)(\w+)')
# regex_addCapTag=re.compile("[A-Z]{3,}")


def removeEmoticons(text):
#    regex_removeEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
    text = regex_removeEmoticons.sub('', text) 
    """ Removes emoticons from text """
    # text = re.sub(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:', '', text)
    return text

def removeHashtagInFrontOfWord(text):
    """ Removes hastag in front of a word """
# #    regex_removeHashtagInFrontOfWord = re.compile(r'#([^\s]+)')
    text = regex_removeHashtagInFrontOfWord.sub(r'\1', text)
    return text

def removeUnicode(text):
    """ Removes unicode strings like "\u002c" and "x96" """
    text = regex_replaceUnicode_match1.sub(r'', text)       
    text = regex_replaceUnicode_match2.sub(r'',text)

#     # text = re.sub(r'(\\u[0-9A-Fa-f]+)',r'', text)       
#     # text = re.sub(r'[^\x00-\x7f]',r'',text)
    return text

def removing_contradictions(text):
    if text.count("n't"):
        text = text.replace("n't", " not")
    text = re.sub("ai\snot", "am not", text)
    text = re.sub("wo\snot", "will not", text)
    return text

def replaceURL(text):
    """ Replaces url address with "url" """
#    regex_replaceURL_match1= re.compile('((www\.[^\s]+)|(https?://[^\s]+))')
#    regex_replaceURL_match2= re.compile('#([^\s]+)')
    # text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',text)
    # text = re.sub(r'#([^\s]+)', r'\1', text)

    # text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',text)

    text = regex_replaceURL_match1.sub('url',text)
    text = regex_replaceURL_match2.sub(r'\1', text)
    # text = re.sub(r'#([^\s]+)', r'\1', text)
    return text


def replaceAtUser(text):
    """ Replaces "@user" with "atUser" """
#    regex_replaceAtUser = re.compile('@[^\s]+')
    text = regex_replaceAtUser.sub('atUser', text)
    return text

def removeCarriageReturns(t):
    if "\n" in t:
        t=t.replace("\n", " ")
    if "\r" in t:
        t=t.replace("\r", " ")
    return t


""" Creates a dictionary with slangs and their equivalents and replaces them """
with open(thisfilelocation + os.path.sep + 'slang.txt') as file:
    slang_map = dict(map(str.strip, line.partition('\t')[::2])
    for line in file if line.strip())

slang_words = sorted(slang_map, key=len, reverse=True) # longest first for regex
regex_for_slangextract = re.compile(r"\b({})\b".format("|".join(map(re.escape, slang_words))))
replaceSlang = partial(regex_for_slangextract.sub, lambda m: slang_map[m.group(1)])

def removeNumbers(text):
    """ Removes integers """
    text = ''.join([i for i in text if not i.isdigit()])         
    return text

def replaceMultiExclamationMark(text):
#    regex_replaceMultiExclamationMark = re.compile(r"(\!)\1+")
    text = regex_replaceMultiExclamationMark.sub(' multiExclamation ', text)
    """ Replaces repetitions of exlamation marks """
    # text = re.sub(r"(\!)\1+", ' multiExclamation ', text)
    return text

def replaceMultiQuestionMark(text):
    """ Replaces repetitions of question marks """
#    regex_replaceMultiQuestionMark = re.compile(r"(\?)\1+")
    text=regex_replaceMultiQuestionMark.sub(' multiQuestion ', text)
    # text = re.sub(r"(\?)\1+", ' multiQuestion ', text)
    return text

def replaceMultiStopMark(text):
#    regex_replaceMultiStopMark = re.compile(r"(\.)\1+")
    text = regex_replaceMultiStopMark.sub(' multiStop ', text)
    """ Replaces repetitions of stop marks """
    # text = re.sub(r"(\.)\1+", ' multiStop ', text)
    return text

contraction_patterns = [ (r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'i\'m', 'i am'), (r'ain\'t', 'is not'), (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'),
                         (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not') ]

def replaceContraction(text):
    patterns = [(re.compile(regex_for_slangextract), repl) for (regex_for_slangextract, repl) in contraction_patterns]
    for (pattern, repl) in patterns:
        (text, count) = re.subn(pattern, repl, text)
    return text


# to be shared with module_text2emotion
def common_clean_tweet(text, to_lower=False):
    # print("cleaning tweet")
    if to_lower:
        print("to lower")
        text = text.lower()
    # import pdb; pdb.set_trace()    
    text = replace_emojis_within_text(text)
    text = convert_multi_char_emoji_to_emotion(text)
    text = removeUnicode(text) # Technique 0
    # text = emojis_extractor(text)
    text = replaceURL(text) # Technique 1
    text = removeHashtagInFrontOfWord(text) # Technique 1
    text = replaceAtUser(text) # Technique 1
    text = removeCarriageReturns(text)
    text = replaceSlang(text) # Technique 2: replaces slang words and abbreviations with their equivalents
    text = replaceContraction(text) # Technique 3: replaces contractions to their equivalents
    text = removeNumbers(text) # Technique 4: remove integers from text
    # todo we need to replace this with emojis
    # text = removeEmoticons(text)
    text = replaceMultiExclamationMark(text) # Technique 5: replaces repetitions of exlamation marks with the tag "multiExclamation"
    text = replaceMultiQuestionMark(text) # Technique 5: replaces repetitions of question marks with the tag "multiQuestion"
    text = replaceMultiStopMark(text) # Technique 5: replaces repetitions of stop marks with the tag "multiStop"
    return text
