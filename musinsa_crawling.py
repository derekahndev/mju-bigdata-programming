import requests
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver

PAGES = 100  # 크롤링할 페이지 수

# 크롤링한 내용을 임시로 저장할 리스트
goods_no_list = []
ranking_list = []

product_title = []  # 상품명
ranking_change = []  # 랭킹 변동
item_category1 = []  # 품목 대분류
item_category2 = []  # 품목 소분류
brand_name = []  # 브랜드명
pageview = []  # 상품 조회수
sales_qty = []  # 누적판매
like = []  # 좋아요 수
rating = []  # 구매 후기 점수
review_count = []  # 구매 후기 수
article_tag_list = []  # 상품 태그 리스트
price = []  # 상품 가격

age_18_ratio = []  # ~18세 구매 비율
age_1923_ratio = []  # 19~23세 구매 비율
age_2428_ratio = []  # 24~28세 구매 비율
age_2933_ratio = []  # 29~33세 구매 비율
age_3439_ratio = []  # 34~39세 구매 비율
age_40_ratio = []  # 40~세 구매 비율

gender_male_ratio = []  # 남성 구매 비율
gender_female_ratio = []  # 여성 구매 비율

n_label = []  # 한정 판매 등 이벤트


# 페이지 내의 크롤링할 상품의 페이지 번호를 가져옴
def get_goods_no_list(url):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        goods = soup.find('ul', id='goodsRankList')
        temp = [item['data-goods-no'] for item in goods.find_all('li', 'li_box')]
        return temp
    else:
        print(response.status_code)
        return


# 상품의 랭킹 변동 값을 가져오는 함수
# 특히 상품의 랭킹 변동은 상품의 상세 페이지가 아닌 랭킹 페이지에 존재하여 따로 가져오도록 함수를 정의함
def get_ranking_list(url):
    temp_ranking_list = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ("
                                "KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.implicitly_wait(3)
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    goods = soup.find('ul', id='goodsRankList')
    for item in goods.find_all('li', 'li_box'):
        rank_up = item.find('span', 'rank up')
        rank = item.find('span', 'rank')
        rank_down = item.find('span', 'rank down')
        if rank_up is not None:
            temp_ranking_list.append(int(rank_up.get_text().split()[1]))
            continue
        if rank_down is not None:
            temp_ranking_list.append(-1 * int(rank_down.get_text().split()[1]))
            continue
        if rank is not None:
            temp_ranking_list.append(0)
            continue

    driver.close()

    return temp_ranking_list


# 가져온 값이 한글 단위로 적혀있을 경우 이를 숫자로 바꾸는 함수
def count_str(str):
    count = str[:-1]
    unit = str[-1]
    if unit == '만':
        return int(float(count) * 10000)
    elif unit == '천':
        return int(float(count) * 1000)
    else:
        return int(count)


# xlsx 파일을 생성하는 함수
def worksheet_init(worksheet):
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('L:L', 50)

    worksheet.write('A1', 'rank')
    worksheet.write('B1', 'ranking_change')
    worksheet.write('C1', 'product_title')
    worksheet.write('D1', 'item_category1')
    worksheet.write('E1', 'item_category2')
    worksheet.write('F1', 'brand_name')
    worksheet.write('G1', 'pageview')
    worksheet.write('H1', 'sales_qty')
    worksheet.write('I1', 'like')
    worksheet.write('J1', 'rating')
    worksheet.write('K1', 'review_count')
    worksheet.write('L1', 'article_tag_list')
    worksheet.write('M1', 'price')

    worksheet.write('N1', 'age_18_ratio')
    worksheet.write('O1', 'age_1923_ratio')
    worksheet.write('P1', 'age_2428_ratio')
    worksheet.write('Q1', 'age_2933_ratio')
    worksheet.write('R1', 'age_3439_ratio')
    worksheet.write('S1', 'age_40_ratio')

    worksheet.write('T1', 'gender_male_ratio')
    worksheet.write('U1', 'gender_female_ratio')

    worksheet.write('V1', 'n_label')


# xlsx 파일에 크롤링한 값을 저장하는 함수
def worksheet_write(i):
    worksheet.write(i + 1, 0, i + 1)
    worksheet.write(i + 1, 1, ranking_change[i])
    worksheet.write(i + 1, 2, product_title[i])
    worksheet.write(i + 1, 3, item_category1[i])
    worksheet.write(i + 1, 4, item_category2[i])
    worksheet.write(i + 1, 5, brand_name[i])
    worksheet.write(i + 1, 6, pageview[i])
    worksheet.write(i + 1, 7, sales_qty[i])
    worksheet.write(i + 1, 8, like[i])
    worksheet.write(i + 1, 9, rating[i])
    worksheet.write(i + 1, 10, review_count[i])
    worksheet.write(i + 1, 11, article_tag_list[i])
    worksheet.write(i + 1, 12, price[i])

    worksheet.write(i + 1, 13, age_18_ratio[i])
    worksheet.write(i + 1, 14, age_1923_ratio[i])
    worksheet.write(i + 1, 15, age_2428_ratio[i])
    worksheet.write(i + 1, 16, age_2933_ratio[i])
    worksheet.write(i + 1, 17, age_3439_ratio[i])
    worksheet.write(i + 1, 18, age_40_ratio[i])

    worksheet.write(i + 1, 19, gender_male_ratio[i])
    worksheet.write(i + 1, 20, gender_female_ratio[i])

    worksheet.write(i + 1, 21, n_label[i])


for page in range(PAGES):
    # 먼저 페이지를 불러와 페이지 내의 상품 상세 페이지 번호와 랭킹 변동 값을 가져옴
    print("loading pages...")

    url = 'https://search.musinsa.com/ranking/best?period=month_3&age=ALL&mainCategory=&subCategory=&leafCategory=&price=&golf=false&newProduct=false&exclusive=false&discount=false&soldOut=false&page={}&viewType=small&priceMin=&priceMax='.format(
        page + 1)
    goods_no_list = get_goods_no_list(url)
    ranking_list = get_ranking_list(url)

    print("page loading complete.")
    print("crawling pages...")

    # 상세 페이지에 있는 정보를 크롤링함
    for i in range(len(goods_no_list)):
        url = 'https://store.musinsa.com/app/goods/{}'.format(goods_no_list[i])

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ("
                                    "KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        driver = webdriver.Chrome('chromedriver', options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(url)

        # 각각의 값들이 존재하지 않는 경우가 너무 많아 대부분의 값들이 존재하지 않는 경우를 예외처리함
        # 값들은 존재하지 않는 경우도 None, 빈 칸 등의 여러 예외가 존재하여 모든 예외에 대하여 처리함
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        temp_product_title = soup.select_one('#page_product_detail > div.right_area.page_detail_product > '
                                             'div.right_contents.section_product_summary > span > em').get_text()
        temp_item_category1 = soup.select_one('#page_product_detail > div.right_area.page_detail_product > '
                                              'div.right_contents.section_product_summary > div.product_info > p > '
                                              'a:nth-child(1)')
        if temp_item_category1 is not None:
            temp_item_category1 = temp_item_category1.get_text()
        temp_item_category2 = soup.select_one('#page_product_detail > div.right_area.page_detail_product > '
                                              'div.right_contents.section_product_summary > div.product_info > p > '
                                              'a:nth-child(2)')
        if temp_item_category2 is not None:
            temp_item_category2 = temp_item_category2.get_text()
        product_article = soup.find('ul', 'product_article')
        temp_brand_name = soup.select_one('#page_product_detail > div.right_area.page_detail_product > '
                                          'div.right_contents.section_product_summary > div.product_info > p > '
                                          'a:nth-child(3)')
        if temp_brand_name is not None:
            temp_brand_name = temp_brand_name.get_text().replace('\n', '').replace(' ', '').replace('(', '').replace(')', '')
        temp_pageview_str = product_article.select_one('strong#pageview_1m')
        if temp_pageview_str:
            if len(temp_pageview_str):
                temp_pageview_str = temp_pageview_str.get_text().split()[0]
                temp_pageview = count_str(temp_pageview_str)
            else:
                temp_pageview = None
        else:
            temp_pageview = None
        temp_sales_qty_str = product_article.select_one('strong#sales_1y_qty')
        if temp_sales_qty_str:
            if len(temp_sales_qty_str):
                temp_sales_qty_str = temp_sales_qty_str.get_text().split()[0]
                temp_sales_qty = count_str(temp_sales_qty_str)
            else:
                temp_sales_qty = None
        else:
            temp_sales_qty = None
        temp_like = product_article.select_one('span.prd_like_cnt')
        if temp_like is not None:
            temp_like = temp_like.get_text()
        temp_rating = product_article.select_one('span.prd-score__rating')
        if temp_rating is not None:
            temp_rating = temp_rating.get_text()
        temp_review_count = product_article.select_one('span.prd-score__review-count')
        if temp_review_count is not None:
            temp_review_count = temp_review_count.get_text().split()[1][:-1]
        temp_product_article_contents = soup.select_one('#product_order_info > '
                                                        'div.explan_product.product_info_section > ul > '
                                                        'li.article-tag-list.list > p')
        if temp_product_article_contents is not None:
            temp_product_article_contents = temp_product_article_contents.get_text()
            temp_article_tag_list = [item[1:] for item in temp_product_article_contents.split()]
        else:
            temp_article_tag_list = None
        temp_price = soup.find('span', id='list_price')
        if temp_price is not None:
            if len(temp_price):
                temp_price = temp_price.get_text()[:-1].split()[0]
            else:
                temp_price = soup.find('span', id='goods_price').get_text()[:-1].split()[0][:-1]
        else:
            temp_price = soup.find('span', id='goods_price').get_text()[:-1].split()[0][:-1]
        temp_age_graph = soup.find('div', 'graph_bar_wrap').find_all('span', 'bar_num')
        if temp_age_graph is not None:
            if len(temp_age_graph[0]):
                temp_age_ratio = [item.get_text() for item in temp_age_graph]
            else:
                temp_age_ratio = [None, None, None, None, None, None]
        else:
            temp_age_ratio = [None, None, None, None, None, None]
        temp_gender_graph = soup.find('div', 'graph_doughnut_wrap').find_all('dd', 'label_info_value')
        if temp_gender_graph is not None:
            if len(temp_gender_graph):
                temp_gender_ratio = [item.get_text() for item in temp_gender_graph]
            else:
                temp_gender_ratio = [None, None]
        else:
            temp_gender_ratio = [None, None]
        temp_n_label = soup.find('span', 'n-label')
        if temp_n_label is not None:
            temp_n_label = temp_n_label.get_text()

        driver.close()

        product_title.append(temp_product_title)
        ranking_change.append(ranking_list[i])
        item_category1.append(temp_item_category1)
        item_category2.append(temp_item_category2)
        brand_name.append(temp_brand_name)
        pageview.append(temp_pageview)
        sales_qty.append(temp_sales_qty)
        like.append(temp_like)
        rating.append(temp_rating)
        review_count.append(temp_review_count)
        tag_list = ''
        
        # 상품의 태그 리스트의 경우 한 번에 가져올 수 없어 각각의 값들을 더해 string 형태로 저장함
        if temp_article_tag_list is not None:
            for tag in temp_article_tag_list:
                tag_list = tag_list + tag + ' '
        article_tag_list.append(tag_list)
        price.append(temp_price)

        age_18_ratio.append(temp_age_ratio[0])
        age_1923_ratio.append(temp_age_ratio[1])
        age_2428_ratio.append(temp_age_ratio[2])
        age_2933_ratio.append(temp_age_ratio[3])
        age_3439_ratio.append(temp_age_ratio[4])
        age_40_ratio.append(temp_age_ratio[5])

        gender_male_ratio.append(temp_gender_ratio[0])
        gender_female_ratio.append(temp_gender_ratio[1])

        n_label.append(temp_n_label)

    # 크롤링 중간에 selenium의 알 수 없는 오류로 인해 끊기는 경우가 발생함
    # 이를 방지하기 위해 매 페이지마다 중간에 계속해서 백업 파일을 생성하도록 설계함
    # 이를 통해 작업이 중단되더라도 백업 파일을 나중에 연결할 수 있게 됨
    filename = 'musinsa_data' + str(page) + '.xlsx'

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    worksheet_init(worksheet)

    for i in range(len(product_title)):
        worksheet_write(i)

    workbook.close()

    # 크롤링 작업이 매우 오래걸리므로 진행 상황 확인을 위해 추가함
    print(f"{page + 1} page work done.")
