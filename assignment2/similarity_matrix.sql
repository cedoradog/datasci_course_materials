create view if not exists D as
 select docid as row_id, 
  term as col_id,
  count as value
 from frequency;

create view if not exists DT as
 select docid as col_id,
  term as row_id,
  count as value
from frequency;

create view if not exists S as
 select D.row_id as row_id, 
  DT.col_id as col_id, 
  sum(D.value * DT.value) as value
 from D, DT
 where D.col_id = DT.row_id --and
  --D.row_id < DT.col_id
 group by D.row_id, DT.col_id;

select row_id, col_id, value
from S
where (row_id = '10080_txt_crude' and
 col_id =  '17035_txt_earn') or
 (row_id =  '17035_txt_earn' and
 col_id = '10080_txt_crude');

drop view D;
drop view DT;
drop view S;
