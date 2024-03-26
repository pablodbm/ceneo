class ProductDetails():
    def __init__(self, product):
        self.product = product
        self.reviews = []
        self.prosCount = 0
        self.consCount = 0

    def setReviews(self, reviews):
        self.reviews = reviews
    def setProsCount(self, prosCount):
        self.prosCount = prosCount
    def setConsCount(self, consCount):
        self.consCount = consCount
