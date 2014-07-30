import MapReduce
import sys

"""
Returns an symetric friendship relation.
Given a set of records, (person, friend), completes the asymmetric
relationships to be symmetric and return it as a set of tuples
(person, friend).
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    For each record (person, friend) generates a record 
    (first_person, second_person).
    """
    # key: first_person (alphabetically)
    # value: second_person
    sorted_record = sorted(record)
    first_person = sorted_record[0]
    second_person = sorted_record[1]
    mr.emit_intermediate(first_person, second_person)

def reducer(first_person, friends):
    """
    For each person count the number of friends
    """
    # key: person
    # value: list of friends, duplicated in symmetric cases
    symmetric_friends = {friend for friend in friends if 
                  friends.count(friend) > 1}
    asymmetric_friends = set(friends) - symmetric_friends
    for friend in asymmetric_friends:
        mr.emit((first_person, friend))
        mr.emit((friend, first_person))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
