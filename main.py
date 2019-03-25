from twitter import TwitterApi
from twitter.analysis import Analysis,RELATED_TWEET_SIMILARITY_THRESHOLD
from eventreader.event_reader_processor import EventReaderProcessor
from textprocess.similarity import similarity
import os;
from flask import Flask, render_template,jsonify 

def parse_twitter_credential():
    #parser = argparse.ArgumentParser(description="Parse Twitter credential");
    #parser.add_argument("--")
    #TODO set real credential
    account = {}
    account[TwitterApi.CONSUMER_KEY_PARAM_NAME] = "consumer key"
    account[TwitterApi.CONSUMER_SECRET_PARAM_NAME] = "consumer secret"
    account[TwitterApi.ACCESS_TOKEN_PARAM_NAME] = "access_token"
    account[TwitterApi.ACCESS_TOKEN_SECRET_PARAM_NAME] = "access token_secret"
    return  account;

app = Flask(__name__)
processResults = []



def process():
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
       searchResultList.append(searchResult);
    
    analysis = Analysis(searchResultList)
    for tweetSearchResult in searchResultList:
        tweetSearchResult["analysisResult"] = analysis.analyze(tweetSearchResult)
        
       
    return searchResultList;
    #return jsonify(tokenized_texts)
    """
    for event in events:
       print(tokenize_text(event.getSubject()))
    """   

@app.route("/")
def showResults():
   processResults = process();
   return jsonify(processResults)

if __name__ == "__main__":
    processResults = process();
    app.run(host='127.0.0.1', port=8080, debug=True)

    
 