import re
from functools import partial
from collections import Counter
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import os
thisfilelocation = os.path.dirname(os.path.abspath(__file__))

from module_commontextcleaning import slang_words
from module_commontextcleaning import regex_words

# regex_replaceUnicode_match1 = re.compile(r'(\\u[0-9A-Fa-f]+)')
# regex_replaceUnicode_match2 = re.compile(r'[^\x00-\x7f]')
# regex_replaceURL_match1= re.compile('((www\.[^\s]+)|(https?://[^\s]+))')
# regex_replaceURL_match2= re.compile('#([^\s]+)')
# regex_replaceAtUser = re.compile('@[^\s]+')
# regex_removeHashtagInFrontOfWord = re.compile(r'#([^\s]+)')
# regex_replaceMultiExclamationMark = re.compile(r"(\!)\1+")
# regex_replaceMultiQuestionMark = re.compile(r"(\?)\1+")
# regex_replaceMultiStopMark = re.compile(r"(\.)\1+")
regex_countMultiExclamationMarks = re.compile(r"(\!)\1+")
regex_countMultiQuestionMarks = re.compile(r"(\?)\1+")
regex_countMultiStopMarks = re.compile(r"(\.)\1+")
regex_countElongated = re.compile(r"(.)\1{2}")
regex_countAllCaps = re.compile("[A-Z0-9]{3,}")
# regex_removeEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
regex_countEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
# regex_words = re.compile(r'\w+') 
regex_addNotTag1 = re.compile(r'\b(?:not|never|no)\b[\w\s]+[^\w\s]', flags=re.IGNORECASE)
regex_addNotTag2 = re.compile(r'(\s+)(\w+)')
regex_addCapTag=re.compile("[A-Z]{3,}")


### Spell Correction begin ###
""" Spell Correction http://norvig.com/spell-correct.html """
def words(text):
#    regex_words = re.compile(r'\w+') 
    return regex_words.findall(text.lower())
    # return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open(thisfilelocation + os.path.sep + 'corporaForSpellCorrection.txt').read()))
sum_words=sum(WORDS.values())

def P(word, N=sum_words): 
    """P robability of `word`. """
    return WORDS[word] / N

def spellCorrection(word): 
    """ Most probable spelling correction for word. """
    return max(candidates(word), key=P)

def candidates(word): 
    """ Generate possible spelling corrections for word. """
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    """ The subset of `words` that appear in the dictionary of WORDS. """
    return set(w for w in words if w in WORDS)

def edits1(word):
    """ All edits that are one edit away from `word`. """
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    """ All edits that are two edits away from `word`. """
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

### Spell Correction End ###

# def removeUnicode(text):
#     """ Removes unicode strings like "\u002c" and "x96" """
#     text = regex_replaceUnicode_match1.sub(r'', text)       
#     text = regex_replaceUnicode_match2.sub(r'',text)

#     # text = re.sub(r'(\\u[0-9A-Fa-f]+)',r'', text)       
#     # text = re.sub(r'[^\x00-\x7f]',r'',text)
#     return text

# def replaceURL(text):
#     """ Replaces url address with "url" """
# #    regex_replaceURL_match1= re.compile('((www\.[^\s]+)|(https?://[^\s]+))')
# #    regex_replaceURL_match2= re.compile('#([^\s]+)')

#     # text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',text)

#     text = regex_replaceURL_match1.sub('url',text)
#     text = regex_replaceURL_match2.sub(r'\1', text)
#     # text = re.sub(r'#([^\s]+)', r'\1', text)
#     return text

# def replaceAtUser(text):
#     """ Replaces "@user" with "atUser" """
# #    regex_replaceAtUser = re.compile('@[^\s]+')
#     text = regex_replaceAtUser.sub('atUser', text)
#     return text

# def removeHashtagInFrontOfWord(text):
#     """ Removes hastag in front of a word """
# #    regex_removeHashtagInFrontOfWord = re.compile(r'#([^\s]+)')
#     text = regex_removeHashtagInFrontOfWord.sub(r'\1', text)
#     return text

# def removeNumbers(text):
#     """ Removes integers """
#     text = ''.join([i for i in text if not i.isdigit()])         
#     return text

# def replaceMultiExclamationMark(text):
# #    regex_replaceMultiExclamationMark = re.compile(r"(\!)\1+")
#     text = regex_replaceMultiExclamationMark.sub(' multiExclamation ', text)
#     """ Replaces repetitions of exlamation marks """
#     # text = re.sub(r"(\!)\1+", ' multiExclamation ', text)
#     return text

# def replaceMultiQuestionMark(text):
#     """ Replaces repetitions of question marks """
# #    regex_replaceMultiQuestionMark = re.compile(r"(\?)\1+")
#     text=regex_replaceMultiQuestionMark.sub(' multiQuestion ', text)
#     # text = re.sub(r"(\?)\1+", ' multiQuestion ', text)
#     return text

# def replaceMultiStopMark(text):
# #    regex_replaceMultiStopMark = re.compile(r"(\.)\1+")
#     text = regex_replaceMultiStopMark.sub(' multiStop ', text)
#     """ Replaces repetitions of stop marks """
#     # text = re.sub(r"(\.)\1+", ' multiStop ', text)
#     return text

def countMultiExclamationMarks(text):
    """ Replaces repetitions of exlamation marks """
    # regex_countMultiExclamationMarks = re.compile(r"(\!)\1+")
    return len(regex_countMultiExclamationMarks.findall(text))
    # return len(re.findall(r"(\!)\1+", text))

def countMultiQuestionMarks(text):
    # regex_countMultiQuestionMarks = re.compile(r"(\?)\1+")
    return len(regex_countMultiQuestionMarks.findall(text))
    # return len(re.findall(r"(\?)\1+", text))

def countMultiStopMarks(text):
    """ Count repetitions of stop marks """
    # regex_countMultiStopMarks = re.compile(r"(\.)\1+")
    return len(regex_countMultiStopMarks.findall(text))
    # return len(re.findall(r"(\.)\1+", text))

def countElongated(text):
    """ Input: a text, Output: how many words are elongated """
    # regex_countElongated = re.compile(r"(.)\1{2}")
    return len([word for word in text.split() if regex_countElongated.search(word)])

def countAllCaps(text):
    """ Input: a text, Output: how many words are all caps """
    # regex_countAllCaps = re.compile("[A-Z0-9]{3,}")
    return len(regex_countAllCaps.findall(text))

    # return len(re.findall("[A-Z0-9]{3,}", text))

def countSlang(text):
    """ Input: a text, Output: how many slang words and a list of found slangs """
    slangCounter = 0
    slangsFound = []
    tokens = nltk.word_tokenize(text)
    for word in tokens:
        if word in slang_words:
            slangsFound.append(word)
            slangCounter += 1
    return slangCounter, slangsFound

""" Replaces contractions from a string to their equivalents """
contraction_patterns = [ (r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'i\'m', 'i am'), (r'ain\'t', 'is not'), (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'),
                         (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not') ]
# def replaceContraction(text):
#     patterns = [(re.compile(regex_for_slangextract), repl) for (regex_for_slangextract, repl) in contraction_patterns]
#     for (pattern, repl) in patterns:
#         (text, count) = re.subn(pattern, repl, text)
#     return text

def replaceElongated(word):
    """ Replaces an elongated word with its basic form, unless the word exists in the lexicon """

    repeat_regexp_replaceElongated = re.compile(r'(\w*)(\w)\2(\w*)')
    repl = r'\1\2\3'
    if wordnet.synsets(word):
        return word
    repl_word = repeat_regexp_replaceElongated.sub(repl, word)
    if repl_word != word:      
        return replaceElongated(repl_word)
    else:       
        return repl_word

# def removeEmoticons(text):
# #    regex_removeEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
#     text = regex_removeEmoticons.sub('', text) 
#     """ Removes emoticons from text """
#     # text = re.sub(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:', '', text)
#     return text

def countEmoticons(text):
    """ Input: a text, Output: how many emoticons """
#    regex_countEmoticons = re.compile(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:')
    return len(regex_countEmoticons.findall(text))
    # return len(re.findall(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:', text))




### Replace Negations Begin ###

def replace(word, pos=None):
    """ Creates a set of all antonyms for the word and if there is only one antonym, it returns it """
    antonyms = set()
    for syn in wordnet.synsets(word, pos=pos):
      for lemma in syn.lemmas():
        for antonym in lemma.antonyms():
          antonyms.add(antonym.name())
    if len(antonyms) == 1:
      return antonyms.pop()
    else:
      return None

def replaceNegations(text):
    """ Finds "not" and antonym for the next word and if found, replaces not and the next word with the antonym """
    i, l = 0, len(text)
    words = []
    while i < l:
      word = text[i]
      if word == 'not' and i+1 < l:
        ant = replace(text[i+1])
        if ant:
          words.append(ant)
          i += 2
          continue
      words.append(word)
      i += 1
    return words

### Replace Negations End ###

# def addNotTag(text):
#     regex_addNotTag1 = re.compile(r'\b(?:not|never|no)\b[\w\s]+[^\w\s]')
#     regex_addNotTag2 = re.compile(r'(\s+)(\w+)')
#     regex_addNotTag3 = re.compile(r'\1NEG_\2')
#     """ Finds "not,never,no" and adds the tag NEG_ to all words that follow until the next punctuation """
#     transformed = regex_addNotTag1.sub( 
#        lambda match: regex_addNotTag2.sub(r'\1NEG_\2', match.group(0)), 
#        text,
#        flags=re.IGNORECASE)
#     return transformed

def addNotTag(text):
#    regex_addNotTag1 = re.compile(r'\b(?:not|never|no)\b[\w\s]+[^\w\s]', flags=re.IGNORECASE)
#    regex_addNotTag2 = re.compile(r'(\s+)(\w+)')
    """ Finds "not,never,no" and adds the tag NEG_ to all words that follow until the next punctuation """
    transformed = regex_addNotTag1.sub(lambda match: regex_addNotTag2.sub(r'\1NEG_\2', match.group(0)),
       text)
    return transformed


# def addNotTag(text):
#     """ Finds "not,never,no" and adds the tag NEG_ to all words that follow until the next punctuation """
#     transformed = re.sub(r'\b(?:not|never|no)\b[\w\s]+[^\w\s]', 
#        lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', match.group(0)), 
#        text,
#        flags=re.IGNORECASE)
#     return transformed

def addCapTag(word):
    """ Finds a word with at least 3 characters capitalized and adds the tag ALL_CAPS_ """
#    regex_addCapTag=re.compile("[A-Z]{3,}")
    # if(len(re.findall("[A-Z]{3,}", word))):
    if(len(regex_addCapTag.findall(word))):
        word = word.replace('\\', '' )
        transformed = regex_addCapTag.sub("ALL_CAPS_"+word, word)
        return transformed
    else:
        return word



# def addCapTag(word):
#     """ Finds a word with at least 3 characters capitalized and adds the tag ALL_CAPS_ """
#     if(len(re.findall("[A-Z]{3,}", word))):
#         word = word.replace('\\', '' )
#         transformed = re.sub("[A-Z]{3,}", "ALL_CAPS_"+word, word)
#         return transformed
#     else:
#         return word

