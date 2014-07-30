import MapReduce
import sys

"""
Returns an symetric friendship relation.
Given a set of records, (person, friend), completes the relation of
friendship to be symmetric and return it as a set of tuples 
(person, friend).
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    For each record (person, friend) generates a record 
    (first_person, (second_person, direction_of_friendship)).
    """
    # key: first_person (alphabetically)
    # value: tuple (second_person, direction_of_friendship)
    sorted_record = sorted(record)
    first_person = sorted_record[0]
    second_person = sorted_record[1]
    if sorted_record == record:
        direction = 1
    else:
        direction = -1
    friendship = [second_person, direction]        
    mr.emit_intermediate(first_person, friendship)

def reducer(first_person, friendships):
    """
    For each person count the number of friends
    """
    # key: person
    # value: friend_record
    sym_friendship = set()
    for friendship_record in friendships:
        second_person = friendship_record[0]
###        if ((second_person, 1) in record or
   #         (second_person, -1) in record):
        new_friendships = {(first_person, second_person), 
                           (second_person, first_person)}
        sym_friendship = sym_friendship.union(new_friendships) 
    for friendship in sym_friendship:
        mr.emit(friendship)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
