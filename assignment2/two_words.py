#!/usr/bin/python
# -*- coding: utf-8 -*-

#Required packages
import sqlite3 as lite
import sys

#Open the database and create a cursor for it
connection = lite.connect('reuters.db')
cursor = connection.cursor()

#Perform the query: PROJECT_{docid, term}(SELECT_{term='world' or term='transactions'}(frequency))
query = cursor.execute('''
 SELECT docid, term
 FROM frequency
 WHERE term = 'transactions' OR
  term = 'world';''')

#Transform the query in a list of records (docid, term)
newDB = query.fetchall()

#docs_'term' set {docid | (docid, 'term') is in newDB}
docs_transactions = set()
docs_world = set()

for record in newDB:
    if record[1] == 'transactions':
        docs_transactions.add(record[0])
    elif record[1] == 'world':
        docs_world.add(record[0])

#docs_both = {docid | (docid, 'transactions') and (docid, 'world') are in newDB}
docs_both = docs_transactions & docs_world
  
#Run your query against your local database and determine the number 
#of records returned.
answer = len(docs_both)

#Print answer
print(answer)

#Not required: Commit the changes to the reuters database
#connection.commit()

#Close connection
connection.close()
