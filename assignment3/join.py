import MapReduce
import sys
import re

"""
Perform a join query. 
Given a set of records, (table, order_id, attributes) where
table can be "Orders" or "LineItem", perform a join of 
"Orders" and "LineItem" by order_id.
And return a set of lists
(order_id, Order_attributes, order_id, LineItem_attributes)
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    """
    For each record, return a tuple (order_id, record).
    """
    # key: order_id
    # value: the whole record
    order_id = record[1]
    #Leave one occurrence for each word
    mr.emit_intermediate(order_id, record)

def reducer(order_id, records):
    """
    For each order_id, perform the cartesian product of the two tables
    and join the resultant records.
    """
    # value (w/o key): joined records
    orders = [record for record in records if record[0] == "order"]
    items =  [record for record in records if record[0] == "line_item"]
    joins = [order + item for item in items for order in orders]
    for record in joins:
        mr.emit(record)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
