SELECT rank, item_category1, item_category2, product_title, brand_name, rating * sales_qty AS rating_ratio
FROM musinsa_data
ORDER BY rating_ratio DESC;