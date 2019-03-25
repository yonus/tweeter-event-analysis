import tweepy
from textprocess.tokenizers import tokenize_text
import datetime,csv;
from itertools import groupby
class TwitterApi:
    CONSUMER_KEY_PARAM_NAME = "consumer_key"
    CONSUMER_SECRET_PARAM_NAME = "consumer_secret"
    ACCESS_TOKEN_PARAM_NAME = "access_token"
    ACCESS_TOKEN_SECRET_PARAM_NAME = "access_token_secret"
    def __init__(self,account):
        auth = tweepy.OAuthHandler(account[self.CONSUMER_KEY_PARAM_NAME],account[self.CONSUMER_SECRET_PARAM_NAME])
        auth.set_access_token(account[self.ACCESS_TOKEN_PARAM_NAME],account[self.ACCESS_TOKEN_SECRET_PARAM_NAME])
        self.__api = tweepy.API(auth)
        
        ##TODO:this code will be removed when online search is available
        self.__tweetGroupByDate = self.readMockTweets()
    
    def search(self ,subject="", date = None):
        if date is None:
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
        searchTerms = self.createSearchTermsFromSubject(subject)
        tweets = []
        if date in self.__tweetGroupByDate:
            tweets = self.__tweetGroupByDate[date]
        
        return {"date":date,"subject":subject,"searchTerms": searchTerms,"tweets":tweets}
       

    def createSearchTermsFromSubject(self, searchText=""):
        searchTermsList  = tokenize_text(searchText,self.getDroppedPosForSearchTerm())
        return (" ").join(searchTermsList)

    @staticmethod
    def getDroppedPosForSearchTerm():
        return ['VERB' , "NUM","SYM","ADP","ADJ"]
    @staticmethod
    def readMockTweets():
        filePath = "tweets_mock.csv"
        with open(filePath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            tweetList = [(row["date"], row["tweet"]) for row in reader]
            tweetGroupBydate= dict((key, list(group)) for key, group in groupby(tweetList, lambda x : x[0]))    
            return tweetGroupBydate
        


      