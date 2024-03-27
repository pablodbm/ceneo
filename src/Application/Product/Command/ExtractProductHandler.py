import uuid
from src.Domain.Helpers.SoupHelper import SoupHelper

class ExtractProductHandler:

    def __init__(self):
        pass

    @staticmethod
    def handle(command):

        soup = SoupHelper.getSoup(SoupHelper.url,command.id)
        if soup is None:
            return None

        title = SoupHelper.getName(soup)
        reviewsCount = SoupHelper.getReviewsCount(soup)
        avgMark = SoupHelper.getAvgMark(soup)

        productId = str(uuid.uuid4())

        ExtractProductHandler.deleteProduct(title)
        ExtractProductHandler.saveProduct(productId,title,avgMark, reviewsCount)

        SoupHelper.getAllReviews(soup, productId)

        return title



    def deleteProduct(title):
        from app import db
        from sqlalchemy import text

        sql_query = text("SELECT id FROM product WHERE title = :title")
        params = {'title': title}
        result = db.session.execute(sql_query, params)
        result = result.fetchone()

        if result is not None:
            sql_query = text("DELETE FROM product WHERE title = :title")
            params = {'title': title}
            db.session.execute(sql_query, params)
            db.session.commit()

            productId = result[0]
            sql_query = text("DELETE FROM review WHERE productId = :productId")
            params = {'productId': productId}

            db.session.execute(sql_query, params)
            db.session.commit()

    def saveProduct(id, title, avgMark, reviewsCount):
        from app import db, Product
        new_product = Product(id=id, title=title, avgMark=avgMark, reviewsCount=reviewsCount)
        db.session.add(new_product)
        db.session.commit()
