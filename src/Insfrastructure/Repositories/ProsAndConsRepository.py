class ProsAndConsRepository:

    def getProsAndConsForReview(reviewId):
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT * FROM pros_and_cons WHERE reviewId = :reviewId")
        params = {'reviewId': reviewId}
        result = db.session.execute(sql_query, params)
        return [dict(zip(result.keys(), row)) for row in result.fetchall()]

    def countProsOrCons(productId, type):
        from app import db
        from sqlalchemy import text
        sql_query = text("SELECT count(distinct text) from pros_and_cons where type=:type AND productId = :productId")
        params = {'type': type, 'productId': productId}
        result = db.session.execute(sql_query, params)
        return result.fetchone()[0]