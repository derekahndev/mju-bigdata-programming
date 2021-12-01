SELECT item_category2, COUNT(item_category2) AS item_cnt, SUM(sales_qty) AS sales_qty
FROM musinsa_data
GROUP BY item_category2
ORDER BY sales_qty DESC;