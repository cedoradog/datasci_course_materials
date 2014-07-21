#!/usr/bin/env python

import json
import sys
import string
from collections import Counter

def has_hashtags(py_line):
    answer = False
    if 'entities' in py_line.keys():
        if type(py_line['entities']) is dict:
            if 'hashtags' in py_line['entities'].keys():
                if py_line['entities']['hashtags'] != []:
                    answer = True
    return answer

def main():
    #Open the downloaded file with tweets in json format
    tweet_file = open(sys.argv[1], "r")
    #Initialize a counter for the hashtags
    hashtag_counter = Counter()
    count=0
    #For every tweet in json format
    for line in tweet_file:
        #Format as python dictionary
        py_line = json.loads(line)
        #If the line has any hashtag
        if has_hashtags(py_line):
            count +=1
            hashtags = py_line['entities']['hashtags']
            #Encode the hashtags in a list with readable characters
            nice_hashtags = [hashtag['text'].encode('utf-8').lower() for hashtag in hashtags]
            #Add the counting of the list to the hashtag_counter
            hashtag_counter += Counter(nice_hashtags)
    for (hashtag, frequency) in hashtag_counter.most_common(10):
        print(hashtag + " " + str(frequency))
    #Not required: number of hashtags and users
    #print(str(len(hashtag_counter)) + " hashtags , written by " + 
    #      str(count) + " users.")
    #Close tweet_file
    tweet_file.close()
    

if __name__ == '__main__':
    main()
