from textprocess.tokenizers import tokenize_text
from operator import itemgetter
import gensim
RELATED_TWEET_SIMILARITY_THRESHOLD = 0.6
NUM_TOPICS = 4

class Analysis:
         
    def __init__(self,searchResults):
          self.__searchResults = searchResults
          self.__saveTopicModel()
    
    def __saveTopicModel(self):
        eventsTweets = []
        for eventSearchResult in self.__searchResults:
            eventTweetCorpus = self.createCorpus(eventSearchResult["tweets"])
            eventsTweets.append(eventTweetCorpus)
        
        self.__dictionary = gensim.corpora.Dictionary(eventsTweets)
        corpus = [self.__dictionary.doc2bow(eventTweet) for eventTweet in eventsTweets]
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word= self.__dictionary, passes=15)
        self.__eventTopicModel = ldamodel
    
    def analyze(self,eventSearchResult = []):
        analysisResults = {}
        eventTweets = eventSearchResult["tweets"]
        if len(eventTweets) is 0:
            analysisResults = "There is no data enough to analyze"
            return analysisResults
        corpus = self.createCorpus(eventTweets)
        sortedWords = self.calcuateWordCountsForEvent(corpus)
        totalWordCount = sum([x[1] for x in sortedWords])
        analysisResults["AverageWordCount"] = totalWordCount/len(eventTweets)
        analysisResults["Top20Words"] = [x[0] for x in sortedWords[:20]]
        analysisResults["Significiant10Words"] = self.findMostSignificiantWordForEvent(eventSearchResult["subject"])
        return analysisResults
     
    def createCorpus(self,eventTweets = []):
        corpus = []
        for tweet in eventTweets:
             corpus.extend(tokenize_text(tweet["text"]))
        return corpus


    def calcuateWordCountsForEvent(self,corpus):
        eventWordCount = {}
        for word in corpus:
            eventWordCount[word] = eventWordCount.get(word,0) +1

        sortedWords = sorted(eventWordCount.items(), key=itemgetter(1), reverse = True)
        return sortedWords

    def findMostSignificiantWordForEvent(self,subject,n=10):
        subjectCorpus = tokenize_text(subject)
        subjectBow = self.__dictionary.doc2bow(subjectCorpus)
    
        for index, score in sorted(self.__eventTopicModel[subjectBow], key=lambda tup: -1*tup[1]):
          significiantWords = [(x[0],float(x[1])) for x in self.__eventTopicModel.show_topic(index,n)]
          return {"max_topic_score":float(score),"words":significiantWords}

        

        


