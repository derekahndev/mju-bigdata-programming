import pandas as pd


df = pd.read_excel('musinsa_data.xlsx', header=0)

df['rank'] = df['rank'].astype('int64')
df['ranking_change'] = df['ranking_change'].astype('int64')
df['product_title'] = df['product_title'].astype('str')
df['item_category1'] = df['item_category1'].astype('str')
df['item_category2'] = df['item_category2'].astype('str')
df['brand_name'] = df['brand_name'].astype('str')
df['pageview'] = df['pageview'].fillna(0).astype('int64')
df['sales_qty'] = df['sales_qty'].fillna(0).astype('int64')
df['like'] = df['like'].str.replace(',', '').fillna(0).astype('int64')
df['rating'] = df['rating'].fillna(0).astype('float')
df['review_count'] = df['review_count'].str.replace(',', '').fillna(0).astype('int64')
df['article_tag_list'] = df['article_tag_list'].astype('str')
df['price'] = df['price'].str.replace(',', '').fillna(0).astype('int64')

df['age_18_ratio'] = df['age_18_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['age_1923_ratio'] = df['age_1923_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['age_2428_ratio'] = df['age_2428_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['age_2933_ratio'] = df['age_2933_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['age_3439_ratio'] = df['age_3439_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['age_40_ratio'] = df['age_40_ratio'].str.replace('%', '').fillna(0).astype('int64')

df['gender_male_ratio'] = df['gender_male_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['gender_female_ratio'] = df['gender_female_ratio'].str.replace('%', '').fillna(0).astype('int64')
df['n_label'] = df['n_label'].astype('str')

print(df.info())
print(df.head())

df.to_csv('musinsa_data.csv', encoding='utf-8')
