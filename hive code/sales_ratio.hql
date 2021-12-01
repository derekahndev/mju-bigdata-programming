SELECT rank, item_category1, item_category2, product_title, brand_name, ROUND(sales_qty / item_like, 3) AS sales_ratio
FROM musinsa_data
ORDER BY sales_ratio DESC;