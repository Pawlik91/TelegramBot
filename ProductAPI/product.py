class Product:
    def __init__(self):
        self.images = []
        self.categoryPaths = []
    brand = ''
    name = ''
    price = -1
    sale = False
    availabe = ''
    articleNo = -1
    url = ''
    images = []
    categoryPaths = []
    categoryAssortment  = ''
    color = ''

    def toString(self):
        val = "brand: " + self.brand + ", name: " + self.name + ", color: ", self.color, ", price " \
        + str(self.price) + ", sale: " + str(self.sale) + ", assortment: " + self.categoryAssortment \
        + ", articleNo: " + str(self.articleNo)
        return val