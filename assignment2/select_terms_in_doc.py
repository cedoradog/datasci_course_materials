#!/usr/bin/python
# -*- coding: utf-8 -*-

#Required packages
import sqlite3 as lite
import sys

#Open the database and create a cursor for it
connection = lite.connect('reuters.db')
cursor = connection.cursor()

#Perform the query: SELECT_{docid='10398_txt_earn'}(frequency)
query = cursor.execute('''
 SELECT *
 FROM frequency
 WHERE docid = '10398_txt_earn';''')

#Run your query against your local database and determine the number 
#of records returned.
answer = len(query.fetchall())

#Print answer
print(answer)

#Not required: Commit the changes to the matrix database
#connection.commit()

#Close connection
connection.close()
