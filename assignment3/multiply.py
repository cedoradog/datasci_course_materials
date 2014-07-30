import MapReduce
import sys
import re

"""
Compute matrix multiplication.
Given two sparse matrices represented as a set of records
(matrix, i, j, val) return its product matrix as a set of
records (i, j, val).
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

nrowsA, ncolsA = 5, 5 
nrowsB, ncolsB = 5, 5
dimA = (nrowsA, ncolsA)
dimB = (nrowsB, ncolsB)
dimAB = (nrowsA, ncolsB)

def mapper(record):
    """
    For each record return a set of pairs (key, info) where the keys
    indicates the (i, j) places where the value will be used in AB 
    product and the info gives the information of the value itself.
    """
    # key: name of matrix and position
    # value: value
    matrix = record[0]
    row, col  = record[1], record[2]
    value = record[3]
    if matrix == "a":
        for colB in range(ncolsB):
            key = (row, colB)
            info = ("a", col, value)
            mr.emit_intermediate(key, info)
    elif matrix == "b":
        for rowA in range(nrowsA):
            key = (rowA, col)
            info = ("b", row, value)
            mr.emit_intermediate(key, info)

def reducer(key, infos):
    """
    Group by key and sum the products of corresponding values
    of both matrices.
    """
    # key: tuple (i, j) w/ the position of the value
    # value: infos about every A and B entry used to compute the 
    #(i, j) entry of the product AB
    row, col = key[0], key[1]
    for info in infos:
        value = sum([infoA[2] * infoB[2] for infoA in infos 
                     for infoB in infos
                     if (infoA[0] == "a" and 
                         infoB[0] == "b" and
                         infoA[1] == infoB[1])])

    record = [row, col, value]
    mr.emit(record)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
