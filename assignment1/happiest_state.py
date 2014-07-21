#!/usr/bin/env python

import json
import sys
import string
import re

'''Take the Python Dictionary of US States and Territories
Disponible en 
http://code.activestate.com/recipes/
577305-python-dictionary-of-us-states-and-territories/'''

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

#Build the dictionary inverse of states that maps state_name:state_code
codes = {states[state_code]:state_code for state_code in states.keys()}

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
    state_code = ''
    if place[-2:] in codes.values():
        state_code = place[-2:]
    elif place[:-5] in codes.keys():
        state_code = codes[place[:-5]]
    return state_code

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
    '''Initialize a dictionary that maps 
    state_code:[state_sentiment, state_cases]'''
    state_sentiment = {state_code:[0, 0] for state_code in codes.values()}
    #For every tweet in json format
    count = 0
    for line in tweet_file:
        #Format as python dictionary
        py_line = json.loads(line)
        #If it is a valid tweet with information about the place
        if has_text(py_line) and has_US_place_full_name(py_line):
            count +=1
            #Encode that tweet in readable characters
            tweet = py_line['text'].encode('utf-8')
            place = str(py_line['place']['full_name'].encode('utf-8'))
            state = find_state(place)
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
            if state != '':
                state_sentiment[state][0] += tweet_score
                state_sentiment[state][1] += 1
    #Calculate the mean of each state score
    mean_state_sentiment = {state:
                            float(state_sentiment[state][0]) / 
                            state_sentiment[state][1] 
                            for state in state_sentiment.keys()
                            if state_sentiment[state][1] != 0}
    max_score, happiest_state = max([mean_state_sentiment[state], state] 
                                    for state in mean_state_sentiment.keys())
    #Not required: Print the content of the state_sentiment and the
    #mean_state_sentiment dictionaries
    # for state in mean_state_sentiment.keys():
    #     print(state + ' ' + str(state_sentiment[state][0]) + ' ' +
    #           str(state_sentiment[state][1]) + ' ' +
    #           str(mean_state_sentiment[state]))
    #Print the happiest_state
    print(happiest_state)
    #Not required: Print the number of tweets taken into account
    #print(str(count) + " tweets registered.")
    #Close tweet_file
    tweet_file.close()    

if __name__ == '__main__':
    main()
