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
    #As a by-product, create a file with every tweet
    text_tweets = open("tweets.txt", "w")
    #For every tweet in json format
    for i, line in enumerate(tweet_file):
        #Format as python dictionary
        py_stru = json.loads(line)
        #If it is a valid tweet
        if 'text' in py_stru.keys():
            #Encode that tweet in readable characters
            tweet = py_stru['text'].encode('utf-8')
            #Write tweet in the text_tweet file
            text_tweets.write(tweet + '\n')
            #Exclude non-letter characters that are not in the sentiment dictionary
            nice_tweet = re.sub('[' + excluded + ']', " ", tweet)
            #Calculate the tweet score
            tweet_score = 0
            #For every word in the tweet
            for term in nice_tweet.lower().split():
                #If term is in the sentimen dictionary...
                if term in sentiment.keys():
                    #add its score to the tweet score
                    tweet_score = tweet_score + sentiment[term]
            #Calculates the total tweet_score
            tweet_sentiment[i] = tweet_score
        #If it is not a valid tweet, tweet_score = NaN
        else:
            tweet_sentiment[i] = float('NaN')
        #Print the tweet score
	print(str(tweet_sentiment[i]))
    text_tweets.close()
    tweet_file.close()
    

if __name__ == '__main__':
    main()
