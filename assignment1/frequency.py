#!/usr/bin/env python

import json
import sys
import string
import re

def main():
    #Create a dictionary with the absolute frequency (number of ocurrences)
    #of a term in all tweets and the total number of words in all tweets
    frequency = {}
    all_words = 0
    #Open the livestream file with tweets in json format
    tweet_file = open(sys.argv[1], "r")
    #Allowed characters in tweets
    allowed = string.lowercase + string.uppercase + " "
    #Excluded characters in tweets
    excluded = string.printable.translate(None, allowed)
    #For every tweet in the livestream data (json format)
    for line in tweet_file:
        #Format as python dictionary
        py_stru = json.loads(line)
        #If it is a valid tweet
        if 'text' in py_stru.keys():
            #Encode that tweet in readable characters
            tweet = py_stru['text'].encode('utf-8')
            #Exclude non-letter characters that are not in the sentiment dictionary
            nice_tweet = re.sub('[' + excluded + ']', " ", tweet)
            terms_in_tweet = nice_tweet.lower().split()
            #For every word in the tweet that is in the sentiment dictionary
            #term:number_of_ocurrences
            for term in terms_in_tweet:
		#Add 1 to the absolute frequency of the term
                if term in frequency.keys():
		    frequency[term] += 1
                else:
                    frequency[term] = 1
                #In every case, add 1 to total of words
                all_words += 1
    #For every term in the tweets
    for term in frequency.keys():
        #Compute and print the relative frequency
	rel_frequency = float(frequency[term]) / all_words
	print(term + ' ' + str(rel_frequency))
    #Close the read file
    tweet_file.close()

if __name__ == '__main__':
    main()
