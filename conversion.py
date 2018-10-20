
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

text = 'Going back to the RCT, as I mentioned, I was involved in developing a new feature for it, which was refresher explorations. This feature, which although served it purpose to some extent, was not a very streamlined approach to the problem, and hence, when I found a project which replaced that with a much better alternative, I thought, this would be the perfect project for me to do. This would also greatly increase the learner experience as currently, with refresher exploration, a lot of redirection to and from pages are present, which could confuse learners, while with Skills, it is going to be played as a part of the exploration itself, and therefore would make the transition to and from a refresher skill seamless.Coming to the introduction of topics and stories to Oppia, to replace collections, these would also greatly increase the sites functionality. One problem, that was seen in the RCT, that could be fixed is that the learner was jumping to later explorations in a collection, without completing the previous ones. With the skills construct added to stories, this could be prevented and as such, make sure that the learner knows all the prerequisites before starting a lesson.'

parser = PlaintextParser.from_string((text), sumytoken(LANGUAGE))
stemmer = Stemmer(LANGUAGE)

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
        
def luhn_summarizer():
    print ("\n","*"*30, "LUHN SUMMARIZER", "*"*30)
    summarizer_luhn = LuhnSummarizer(stemmer)
    summarizer_luhn.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer_luhn(parser.document, SENTENCES_COUNT):
        print (sentence)
        
def gensim_summarizer():
    print ("\n","*"*30, "GENSIM SUMMARIZER", "*"*30)
    print (summarize(text))

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
lexrank_summarizer()
lsa_summarizer()
luhn_summarizer()
gensim_summarizer()
pytldr_textrank()
pytldr_lsa()
