SELECT brand_name, COUNT(brand_name) AS brand_cnt, SUM(sales_qty) AS sales_qty
FROM musinsa_data
GROUP BY brand_name
ORDER BY sales_qty DESC;