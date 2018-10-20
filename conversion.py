
from gensim.summarization import summarize

from sumy.summarizers import luhn
from sumy.utils import get_stop_words
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.luhn import LuhnSummarizer 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer as sumytoken
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer

from pytldr.nlp.tokenizer import Tokenizer as pltdrtoken
from pytldr.summarize.textrank import TextRankSummarizer
from pytldr.summarize.relevance import RelevanceSummarizer
from pytldr.summarize.lsa import LsaSummarizer, LsaOzsoy, LsaSteinberger


LANGUAGE = "english"
SENTENCES_COUNT = 2


def lexrank_summarizer():
    print("\n","*"*30, "LEXRANK SUMARIZER", "*"*30)
    summarizer_LexRank = LexRankSummarizer(stemmer)
    summarizer_LexRank.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer_LexRank(parser.document, SENTENCES_COUNT):
        print (sentence)
        
def lsa_summarizer():
    print ("\n","*"*30, "LSA SUMMARIZER", "*"*30)
    summarizer_lsa = Summarizer(stemmer)
    summarizer_lsa.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer_lsa(parser.document, SENTENCES_COUNT):
        print (sentence)
        
def luhn_summarizer(data):
    text = data
    parser = PlaintextParser.from_string((text), sumytoken(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)    
    print ("\n","*"*30, "LUHN SUMMARIZER", "*"*30)
    summarizer_luhn = LuhnSummarizer(stemmer)
    summarizer_luhn.stop_words = get_stop_words(LANGUAGE)
    result = ''
    for sentence in summarizer_luhn(parser.document, SENTENCES_COUNT):
        result += str(sentence)
    
    return result
        
def gensim_summarizer(data):
    text = data
    print ("\n","*"*30, "GENSIM SUMMARIZER", "*"*30)
    print (summarize(text))
    return summarize(text)

def pytldr_textrank():
    print ("\n","*"*30, "PYTLDR TEXTRANK", "*"*30)
    tokenizer = pltdrtoken('english')
    summarizer = TextRankSummarizer(tokenizer)
    summarizer = TextRankSummarizer() 
    summary = summarizer.summarize(text, length=4)
    print (summary)

def pytldr_lsa():
    print ("\n","*"*30, "PYTLDR LSA", "*"*30)
    summarizer = LsaOzsoy()
    summarizer = LsaSteinberger()
    summarizer = LsaSummarizer()  # This is identical to the LsaOzsoy object

    summary = summarizer.summarize(
        text, topics=4, length=5, binary_matrix=True, topic_sigma_threshold=0.5
    )
    print (summary)

#----Call all the functions to compare the summaries
# lexrank_summarizer()
# lsa_summarizer()
# luhn_summarizer()
# gensim_summarizer()
# pytldr_textrank()
# pytldr_lsa()
