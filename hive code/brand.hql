SELECT brand_name, COUNT(brand_name) AS brand_cnt
FROM musinsa_Data
GROUP BY brand_name
ORDER BY brand_cnt DESC;