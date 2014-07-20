#!/usr/bin/env python

import json
import sys
import string
import re
from state_codes2names import states

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def has_text(py_line):
    answer = False
    if 'text' in py_line.keys():
        answer = True
    return answer

def has_US_place_full_name(py_line):
    answer = False
    if 'place' in py_line.keys():
        if type(py_line['place']) is dict:
            if 'full_name' and 'country_code' in py_line['place'].keys():
                if py_line['place']['country_code'].encode('utf-8') == 'US':
                    answer = True
    return answer

def find_state(place):
    state_name = ''
    if place[-2:] in states.keys():
        state_name = states[place[-2:]]
    elif place[:-5] in states.values():
        state_name = place[:-5]
    return state_name

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
    #Initialize a dictionary that maps state_name:state_sentiment
    state_sentiment = {state_name:0 for state_name in states.values()}
    count = 0
    #For every tweet in json format
    for line in tweet_file:
        #Format as python dictionary
        py_line = json.loads(line)
        #If it is a valid tweet with information about the place
        if has_text(py_line) and has_US_place_full_name(py_line):
            count +=1
            #Encode that tweet in readable characters
            tweet = py_line['text'].encode('utf-8')
            place = str(py_line['place']['full_name'].encode('utf-8'))
            state_name = find_state(place)
            #Exclude non-letter characters
            nice_tweet = re.sub('[' + excluded + ']', " ", tweet)
            #Calculate the tweet score
            tweet_score = 0
            #For every word in the tweet
            for term in nice_tweet.lower().split():
                #If term is in the sentimen dictionary...
                if term in sentiment.keys():
                    #add its score to the tweet score
                    tweet_score = tweet_score + sentiment[term]
            #Add the total tweet_score to the state_sentiment
            if state_name != '':
                state_sentiment[state_name] += tweet_score
    max_score, happiest_state = max([state_sentiment[state], state] for state in state_sentiment.keys())
    #Not required: Print the content of the state_sentiment dictionary
    #for state in state_sentiment.keys():
    #    print(state + " " + str(state_sentiment[state]))
    print happiest_state
    print count
    #Close tweet_file
    tweet_file.close()
    

if __name__ == '__main__':
    main()
