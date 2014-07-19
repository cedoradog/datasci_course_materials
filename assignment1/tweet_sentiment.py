#!/usr/bin/env python

import json
import sys
import string
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def create_sent_scoring(sent_file_dir):
    sent_file = open(sent_file_dir, "r")
    sentiment = {}
    for line in sent_file:
        term, score = line.split("\t")
        sentiment[term] = int(score)
    sent_file.close()
    return sentiment

def main():
    #Create a dictionary with the scoring of known terms
    sentiment = create_sent_scoring(sys.argv[1])
    #Open the downloaded file with tweets in json format
    tweet_file = open(sys.argv[2], "r")
    #Allowed characters in tweets
    allowed = string.lowercase + string.uppercase + " "
    #Excluded characters in tweets
    excluded = string.printable.translate(None, allowed)
    #Initialize a dictionary that maps line_number:tweet_score
    tweet_sentiment = {}
    #Initailize a file to save the score of each tweet
#    score_tweets = open("sentiment_tweets.txt", "w")
    #As a by-product, create a file with every tweet
    text_tweets = open("tweets.txt", "w")
#    as_list_tweets = list(tweet_file)
    for i, line in enumerate(tweet_file):
        py_str = json.loads(line)
        if 'text' in py_str.keys():
            tweet = py_str['text'].encode('utf-8')
            text_tweets.write(tweet + '\n')
            nice_tweet = re.sub('[' + excluded + ']', " ", tweet)
            tweet_score = 0
            for term in tweet.lower().split():
                if term in sentiment.keys():
                    tweet_score = tweet_score + sentiment[term]
            tweet_sentiment[i] = tweet_score
        else:
            tweet_sentiment[i] = float('NaN')
	print(str(tweet_sentiment[i]) + '\n')
 #       score_tweets.write(str(tweet_sentiment[i]) + '\n')
#    score_tweets.close()
    text_tweets.close()
    tweet_file.close()
    

if __name__ == '__main__':
    main()
