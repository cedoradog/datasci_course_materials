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
    non_sentiment = {}
    #Open the downloaded file with tweets in json format
    tweet_file = open(sys.argv[2], "r")
    #Allowed characters in tweets
    allowed = string.lowercase + string.uppercase + " "
    #Excluded characters in tweets
    excluded = string.printable.translate(None, allowed)
    #Initialize a dictionary that maps line_number:tweet_score
    tweet_sentiment = {}
    #For every tweet in json format
    for line in tweet_file:
        #Format as python dictionary
        py_stru = json.loads(line)
        #If it is a valid tweet
        if 'text' in py_stru.keys():
            #Encode that tweet in readable characters
            tweet = py_stru['text'].encode('utf-8')
            #Exclude non-letter characters that are not in the sentiment dictionary
            nice_tweet = re.sub('[' + excluded + ']', " ", tweet)
      	    #List of the terms in the tweet
	    terms_in_tweet = set(nice_tweet.lower().split())
      	    #Terms can be or not to be in the sentiment dictionary
	    sent_terms = terms_in_tweet.intersection(sentiment.keys())
	    non_sent_terms = terms_in_tweet.difference(sentiment.keys())
            #Calculate the tweet score
            tweet_score = 0
            #For every word in the tweet that is in the sentiment dictionary
            for term in sent_terms:
                #Add its score to the tweet score
                tweet_score = tweet_score + sentiment[term]		    
            #Use the tweet score to assign a score to the others terms of the tweet
            for term in non_sent_terms:
	    #Build a dictionary non_sentiment that maps 
	    #term:[sum_of_tweets_scores, number_of_tweets]
		if term in non_sentiment.keys():
		    non_sentiment[term][0] = non_sentiment[term][0] + tweet_score
		    non_sentiment[term][1] = non_sentiment[term][1] + 1
		else:
		    non_sentiment[term] = [tweet_score, 1]
    #For every term with a new score assigned
    for term in non_sentiment.keys():
	term_score = float(non_sentiment[term][0])/non_sentiment[term][1]
	print(term + ' ' + str(round(term_score, 2)))
    tweet_file.close()
    

if __name__ == '__main__':
    main()
