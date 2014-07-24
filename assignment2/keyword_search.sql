create table if not exists query(
 docid varchar(255),
 term char(255),
 count int,
 primary key(docid, term));

insert into query
values ('query', 'washington', 1); 

insert into query
values ('query', 'taxes', 1);

insert into query
values ('query', 'treasury', 1);

create view if not exists q as
 select docid as row_id, 
  term as col_id,
  count as value
 from query;

create view if not exists DT as
 select docid as col_id,
  term as row_id,
  count as value
from frequency;

create view if not exists r as
 select q.row_id as row_id, 
  DT.col_id as col_id, 
  sum(q.value * DT.value) as value
 from q, DT
 where q.col_id = DT.row_id
 group by q.row_id, DT.col_id;

select max(value)
 from (
  select value
  from r);

drop table query;
drop view q;
drop view DT;
drop view r;
