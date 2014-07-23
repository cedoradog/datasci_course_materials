#!/usr/bin/python
# -*- coding: utf-8 -*-

#Required packages
import sqlite3 as lite
import sys

#Open the database and create a cursor for it
connection = lite.connect('reuters.db')
cursor = connection.cursor()

#Perform the query: PROJECT_docid(SELECT_{sum(count)>300}(frequency_{GROUP BY docid}))
query = cursor.execute('''
 SELECT docid
 FROM frequency
 GROUP BY docid
 HAVING sum(count) > 300;''')

#Run your query against your local database and determine the number 
#of records returned.
answer = len(query.fetchall())

#Print answer
print(answer)

#Not required: Commit the changes to the reuters database
#connection.commit()

#Close connection
connection.close()
