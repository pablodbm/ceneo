from src.Insfrastructure.Repositories.ProsAndConsRepository import ProsAndConsRepository
class ReviewRepository:
    @staticmethod
    def getReviewsByProductId(productId):
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT * FROM review WHERE productId = :productId")
        params = {'productId': productId}
        result = db.session.execute(sql_query, params)
        reviews = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        for review in reviews:
            review['prosAndCons'] = ProsAndConsRepository.getProsAndConsForReview(review['id'])
        return reviews

    @staticmethod
    def countForProductId(productId):
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT count(id) FROM review WHERE productId = :productId")
        params = {'productId': productId}
        result = db.session.execute(sql_query, params)
        return result.fetchone()[0]

    @staticmethod
    def getReviewsForProductId(productId):
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT * FROM review WHERE productId = :productId")
        params = {'productId': productId}
        result = db.session.execute(sql_query, params)
        return [dict(zip(result.keys(), row)) for row in result.fetchall()]
