import MapReduce
import sys

"""
Count the number of friends of a person.
Given a set of records, (person, friend), get the number of
friend of a person and return a set of tuples (person, friend_count)
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    For each record (person, friend) generates a record (person, 1)
    """
    # key: person
    # value: 1
    person = record[0]
    mr.emit_intermediate(person, 1)

def reducer(person, friend_record):
    """
    For each person count the number of friends
    """
    # key: person
    # value: friends count
    friend_count = sum(friend_record)
    mr.emit((person, friend_count))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
