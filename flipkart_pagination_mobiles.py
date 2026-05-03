from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from time import sleep
import pandas as pd

root_url = 'https://www.flipkart.com'

all_tags = []
img_src = []
prod_names = []
prod_ratings = []
prod_prices = []
prod_descriptions = []
prod_reviews = []

for i in range(1, 11):
    sleep(2)
    print()
    np_path = f'/search?q=mobiles+under+50000&amp;otracker=search&amp;otracker1=search&amp;marketplace=FLIPKART&amp;as-show=on&amp;as=off&amp;page={i}'
    url = root_url+np_path
    user_agent = UserAgent(os='desktop')
    header = {'User-Agent': user_agent.chrome}
    resp = requests.get(url, headers=header)
    html = resp.text
    root_soup = BeautifulSoup(html, 'html.parser')
    print(resp)
    
    for tags in root_soup.find_all('div', class_='jIjQ8S'):
        #print(tags)
        all_tags.append(tags)
    
        for img in tags.find_all('img', class_='UCc1lI'):
            src = img.get('src') 
            img_src.append(src)
            print(src)
    
        for prod in tags.find_all('div', class_="RG5Slk"):
            name = prod.text.strip()
            prod_names.append(name)
            print(name)
    
        for rating in tags.find_all('div', class_= 'MKiFS6'):
            rate = rating.text.strip()
            prod_ratings.append(rate)
            print(rate)
        
        for price in tags.find_all('div', class_='DeU9vF'):
            prod_price = price.text.strip()
            prod_prices.append(prod_price)
            print(prod_price)
    
        for desc in tags.find_all('ul', class_='HwRTzP'):
            prod_desc = desc.text.strip()
            prod_descriptions.append(prod_desc)
            #print(prod_desc)
    
        for review in tags.find_all('span', class_='o2SIOJ'):
            review = list(review.parent.children)[-1].text.strip()
            print(review)
            prod_reviews.append(review)


df = pd.DataFrame(
        {
        'Product names': prod_names, 
        'Product ratings': prod_ratings, 
        'Product prices': prod_prices,
        'Product Img source': img_src,
        'Product Description': prod_descriptions,
        'Product Reviews': prod_reviews
        }
    )

print(df)

df.to_excel('flipkart_multi_page_products.xlsx', index=False, sheet_name='Flipkart Products Data')


print('Total data:', len(all_tags))
print('Total img src:', len(img_src))
print('Total products:', len(prod_names))
print('Total ratings:', len(prod_ratings))
print('Total prices:', len(prod_prices))
print('Total Descriptions:', len(prod_descriptions))
print('Total Reviews:', len(prod_reviews))