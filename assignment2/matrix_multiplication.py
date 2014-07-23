#!/usr/bin/python
# -*- coding: utf-8 -*-

#Required packages
import sqlite3 as lite
import sys

#Dimension of the product AB
rowsA = 5
colsB = 5

#Every possible (duplicated) tuple for of product
dimAB = [(i, j, i, j) for i in range(rowsA) for j in range(colsB)]

#Open the database and create a cursor for it
connection = lite.connect('matrix.db')
cursor = connection.cursor()

#Create the table product
cursor.execute('''
CREATE TABLE product(
 row_num int, 
 col_num int, 
 value int, 
 primary key (row_num, col_num));''')

#Compute the ij-element of AB for every i,j in dimAB
cursor.executemany('''
INSERT INTO product 
VALUES(?, ?, (
 SELECT sum(a.value * b.value) 
 FROM a, b 
 WHERE a.row_num = ? AND
  b.col_num = ? AND
  a.col_num = b.row_num));''', dimAB)

#Get the query: "turn in a text document multiply.txt with a single line 
#containing the value of the cell (2,3)"
query = cursor.execute('''SELECT value
 FROM product
 WHERE row_num = 2 AND
  col_num = 3;''')

#If the query is None, then answer = 0
answer = query.fetchone()[0]
if answer is None:
 answer = 0

#Print answer
print answer

#Delete table product
cursor.execute("DROP TABLE product;")

#Not required: Commit the changes to the matrix database
#connection.commit()

#Close connection
connection.close()
