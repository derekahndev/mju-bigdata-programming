SELECT item_category2, COUNT(item_category2) AS item_cnt
FROM musinsa_data
GROUP BY item_category2
ORDER BY item_cnt DESC;