import urllib,json
from product import Product

_url = 'http://10.1.141.181:3000/products?'

def createURL(brand='', name='', priceFrom='', priceTo='', sale=False, available=False, color=''):
    url1 = _url
    if brand != '':
        url1 = url1 + '&brand=' + brand
    if name != '':
        url1 = url1 + '&name=' + name
    if priceFrom != '':
        url1 = url1 + '&priceFrom=' + priceFrom
    if priceTo != '':
        url1 = url1 + '&priceTo=' + priceTo
    if sale == True:
        url1 = url1 + '&sale=true'
    if available == True:
        url1 = url1 + '&available=true'
    if color != '':
        url1 = url1 + '&color=' + color
        
    return url1

def appendPage(url, pageNo):
    url = url + '&page=' + str(pageNo)
    return url
        
def getDataFromURL(url):
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data

def getProducts(url):
    data = getDataFromURL(url)
    products = data['products']
    return products

def getPageCount(url):
    data = getDataFromURL(url)
    meta = data['meta']
    return meta['pages']

def createProduct(productData):
    p = Product()

    try:
        p.brand = productData['brand']['name']
    except:
        p.brand = ''

    try:
        p.name = productData['variations'][0]['name']
    except:
        p.name = ''

    try:
        p.price = float(productData['variations'][0]['price']['retailPrice']) / 100
    except:
        p.price = -1
    
    try:
        p.sale = bool(productData['variations'][0]['price']['sale'])
    except:
        p.sale = False

    try:
        p.available = productData['variations'][0]['availability']['code']
    except:
        p.availabe = ''

    try:
        p.articleNo = productData['variations'][0]['articleNumber']
    except:
        p.articleNo = -1
    
    try:
        p.url = productData['variations'][0]['productUrl']
    except:
        p.url = ''
    
    try:
        p.color = productData['variations'][0]['dimensions'][0]['baseColor']
    except:
        p.color = ''

    try:
        img = productData['variations'][0]['images']
        for i in range(0, len(img)):
            p.images.append(img[i]['id'])
    except:
        img = ''
        
    try:
        cat = productData['categories']
        for i in range(0, len(cat)):
            p.categoryPaths.append(cat[i]['path'])
        
        p.categoryAssortment = cat[0]['assortment']
    except:
        p.categoryAssortment = ''

    return p

def createProducts(data):
    products = []
    for i in range(0, len(data)):
        p = createProduct(data[i])
        products.append(p)
    return products

def getAllProducts(brand='', name='', priceFrom='', priceTo='', sale=False, available=False, color=''):
    url = createURL(brand,name,priceFrom,priceTo, sale, available, color)
    pages = getPageCount(url)
    products = []
    for i in range(1, pages + 1):
        cUrl = appendPage(url, i)
        data = getProducts(cUrl)
        products.extend(createProducts(data))

    return products


# products = getAllProducts(brand = "LG", name = "TV")
# print len(products)

# print products[4].name
