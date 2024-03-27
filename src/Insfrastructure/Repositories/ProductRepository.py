from src.Application.Product.Query.ProductDetails import ProductDetails
from src.Insfrastructure.Repositories.ReviewRepository import ReviewRepository
from src.Insfrastructure.Repositories.ProsAndConsRepository import ProsAndConsRepository
from src.Domain.ProsAndCons.ProsAndConsEnum import ProsAndConsEnum

class productRepository:
    @staticmethod
    def query(productTitle, request):
        productDetails = productRepository.getProductByTitle(productTitle)
        if productDetails is None:
            return None
        productDetailsView = ProductDetails(productDetails)
        productDetailsView.reviews = ReviewRepository.getReviewsByProductId(productDetailsView.product['id'], request)
        productDetailsView.setProsCount(ProsAndConsRepository.countProsOrCons(productDetailsView.product['id'],ProsAndConsEnum.pros))
        productDetailsView.setConsCount(ProsAndConsRepository.countProsOrCons(productDetailsView.product['id'],ProsAndConsEnum.cons))
        return productDetailsView



    def getProductByTitle(productTitle):
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT * FROM product WHERE title = :title")
        params = {'title': productTitle}
        result = db.session.execute(sql_query, params)
        results_as_dict = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        if len(results_as_dict) == 0:
            return None
        return results_as_dict[0]
    @staticmethod
    def getAllProducts():
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT * FROM product")
        result = db.session.execute(sql_query)
        products = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        for product in products:
            product['countReviews'] = ReviewRepository.countForProductId(product['id'])
            product['prosCount'] = ProsAndConsRepository.countProsOrCons(product['id'],ProsAndConsEnum.pros)
            product['consCount'] = ProsAndConsRepository.countProsOrCons(product['id'],ProsAndConsEnum.cons)
        return products
