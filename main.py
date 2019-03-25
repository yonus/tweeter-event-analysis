from twitter import TwitterApi
from twitter.analysis import Analysis,RELATED_TWEET_SIMILARITY_THRESHOLD
from eventreader.event_reader_processor import EventReaderProcessor
from textprocess.similarity import similarity
from flask import Flask, render_template,jsonify 
import os

def parse_twitter_credential():
    #TODO set real credential
    account = {}
    account[TwitterApi.CONSUMER_KEY_PARAM_NAME] = "consumer key"
    account[TwitterApi.CONSUMER_SECRET_PARAM_NAME] = "consumer secret"
    account[TwitterApi.ACCESS_TOKEN_PARAM_NAME] = "access_token"
    account[TwitterApi.ACCESS_TOKEN_SECRET_PARAM_NAME] = "access token_secret"
    return  account;


app = Flask(__name__)


class Processor:

   def __init__(self):
      self.__cachedProcessResult = self.process();
   
   def process(self):
      twitterAccount = parse_twitter_credential()
      twitterApi = TwitterApi(twitterAccount)
      eventReaderProcessor = EventReaderProcessor(os.path.abspath("./events.csv"))
      events = eventReaderProcessor.process()
      searchResultList = []
      
      for e in events:
         searchResult = twitterApi.search(e.getSubject(),e.getDate())
         tweets = searchResult["tweets"]
         tweets = [{"similarity":similarity(e.getSubject(),tweet[1]) ,"text":tweet[1]} for tweet in tweets]
         searchResult["tweets"] = list(filter(lambda tweet: tweet["similarity"] > RELATED_TWEET_SIMILARITY_THRESHOLD, tweets))
         searchResultList.append(searchResult)
      
      analysis = Analysis(searchResultList)
      for tweetSearchResult in searchResultList:
         tweetSearchResult["analysisResult"] = analysis.analyze(tweetSearchResult)
         
      return searchResultList

   def getProcessResult(self):
      return self.__cachedProcessResult

   def setProcessResult(self,processResults):
      self.__cachedProcessResult = processResults

processor = Processor()

@app.route("/")
def showResults():
   processResults = processor.getProcessResult()
   return jsonify(processResults)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

    
 