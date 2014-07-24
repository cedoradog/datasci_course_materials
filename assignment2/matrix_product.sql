CREATE VIEW product AS
 SELECT A.row_num AS row_num, 
  B.col_num AS col_num, 
  sum(A.value * B.value) as value
 FROM A, B
 WHERE A.col_num = B.row_num
 GROUP BY A.row_num, B.col_num;

SELECT value
FROM product
WHERE row_num = 2 AND
 col_num = 3;

DROP VIEW product;
