import spacy
nlp = spacy.load('en_core_web_sm')


def similarity(subject = "", tweet = ""):
  print (tweet)
  #cleared_subject = tokenizers.tokenize_text(subject)
  tweet_doc = nlp(tweet)
  return tweet_doc.similarity(nlp(subject))