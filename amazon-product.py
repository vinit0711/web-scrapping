import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_product_title(soup):
    try:
        title = soup.find("span", attrs={
            'id': 'productTitle'}).text.strip()
    except AttributeError:
        title = ""
    return title


def get_no_discount_product_price(soup):
    try:
        no_discount_price = soup.find("span", attrs={
            'class': 'basisPrice'}).find("span", attrs={
            'class': 'a-offscreen'}).text.strip()
    except AttributeError:
        no_discount_price = ""
    return no_discount_price


def get_discounted_product_price(soup):
    try:
        discounted_product_price = soup.find("span", attrs={
            'class': 'priceToPay'}).find("span", attrs={
            'class': 'a-offscreen'}).text.strip()
    except AttributeError:
        discounted_product_price = ""
    return discounted_product_price

if __name__ == '__main__':
    URL = 'https://www.amazon.in/s?k=redmi+phone&crid=1TNW7ZUA9BDOH&sprefix=redmi+phone%2Caps%2C219&ref=nb_sb_noss_1'
    HEADERS = {
        'Accept-Language': 'en-US;q=0.9,en;q=0.5',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    web_page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(web_page.content, 'html.parser')
    product_links = soup.find_all("a", attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    # product_link = all_product_links[0].get('href')
    all_products_links=[]
    for product_link in product_links:
        all_products_links.append(product_link.get('href'))
    d = {"title":[], "MRP":[], "discounted_price":[]}
    for link in all_products_links:
        single_product_link = "https://amazon.in" + link
        print(single_product_link)
        # Now we are able to create product link for each product , Next will have to open each product

        single_product_page = requests.get(single_product_link, headers=HEADERS)
        product_soup = BeautifulSoup(single_product_page.content, 'html.parser')
        # Function calls to display all necessary product information
        d['title'].append(get_product_title(product_soup))
        d['MRP'].append(get_no_discount_product_price(product_soup))
        d['discounted_price'].append(get_discounted_product_price(product_soup))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', pd.np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(amazon_df)

