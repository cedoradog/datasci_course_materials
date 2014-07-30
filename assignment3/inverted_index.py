import MapReduce
import sys
import re

"""
Create an Inverted index. 
Given a set of documents, an inverted index is a dictionary 
where each word is associated with a list of the document 
identifiers in which that word appears.
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    For each doc, return a set of (word, doc_id) pairs for words
    present in the doc.
    """
    # key: document identifier
    # value: document contents
    doc_id = record[0]
    #text = re.sub(r'[^\w]', ' ', record[1])
    text = record[1]
    words = text.split()
    #Leave one occurrence for each word
    unique_words = set(words)
    for word in unique_words:
      mr.emit_intermediate(word, doc_id)

def reducer(word, doc_ids):
    """
    Do nothing. Return the list of doc_ids associated w/ each word.
    """
    # key: word
    # value: list of doc ids where word is
    mr.emit((word, doc_ids))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
