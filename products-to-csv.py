from os import path
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

BASE_URL = "https://www.plazavea.com.pe/"
UNITS_OF_MEASUREMENT = ('un', 'g', 'kg', 'ml', 'l')

def get_products_from_url (url):

    client = urlopen(url)
    page_html = client.read()
    client.close()

    page_soup = soup(page_html, "html.parser")

    arrProductName = []
    arrProductPrice = []

    for div in page_soup.findAll("a", { "class": "Showcase__name" }):
        arrProductName.append(div.text.strip())

    for div in page_soup.findAll("div", { "class": "Showcase__priceBox__amount" }):
        inner_div = div.find("div", { "class": "Showcase__salePrice" })
        arrProductPrice.append(inner_div.text.strip()[3:])    

    return arrProductName, arrProductPrice

def split_name_quantity (raw_name):
    arrName = raw_name.rsplit(' ', 1)
    return arrName[0], arrName[1]    

def preprocess_products (productsName, productsPrice, category):

    # Sometimes list productsName may be larger than the
    # list productsPrice, this is because website renders
    # products even if they are out of stock, however they
    # do not render their price

    arrProducts = []
    minLength = min(len(productsName), len(productsPrice))

    for i in range(minLength):

        word_endings_1 = productsName[i][-1:].lower()
        word_endings_2 = productsName[i][-2:].lower()

        if word_endings_2 in UNITS_OF_MEASUREMENT:
            productName = productsName[i][:-2]
            name, quantity = split_name_quantity(productName)
            ending = word_endings_2
        elif word_endings_1 in UNITS_OF_MEASUREMENT:
            productName = productsName[i][:-1]
            name, quantity = split_name_quantity(productName)
            ending = word_endings_1
        else:
            name = productsName[i]
            quantity = '1'
            ending = 'un'

        if (quantity.replace('.','',1).isdigit()):
            arrProducts.append(','.join([name, productsPrice[i], str(quantity), ending]))
        else:
            print('Quantity is NaN')

    return arrProducts


def save_to_csv (products, category):
    headers = 'Name, Price, Quantity, Unit' + '\n'
    dist_dir = path.join('./data/', category + '.csv')
    with open(dist_dir, mode='w') as f:
        f.write(headers)
        for product in products:
            f.write(product + '\n')   

def products_to_csv (category):
    url = path.join(BASE_URL, category)
    productsName, productsPrice = get_products_from_url(url)
    products = preprocess_products(productsName, productsPrice, category)
    save_to_csv(products, category)

def main ():
    with open('categories.txt') as f:
        categories = f.read().splitlines()
    for category in categories:
        print(f'Saving ... {category}')
        products_to_csv(category)

if __name__ == '__main__':
    main()