from src.Insfrastructure.Repositories.ProsAndConsRepository import ProsAndConsRepository
class ReviewRepository:
    @staticmethod
    def getReviewsByProductId(productId,request):
        from app import db
        from sqlalchemy import text
        sql_query = ''
        if request.args.get('sortBy') and request.args.get('orderBy'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId ORDER BY ' + request.args.get('sortBy') + ' ' + request.args.get('orderBy'))
            params = {'productId': productId}
        elif request.args.get('starsFrom') and request.args.get('starsTo'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId AND stars >= :starsFrom AND stars <= :starsTo')
            params = {'productId': productId, 'starsFrom': request.args.get('starsFrom', '0'), 'starsTo': request.args.get('starsTo', '5')}
        elif request.args.get('authorName'):
            sql_query = text("SELECT * FROM review WHERE productId = :productId AND author LIKE '%' || :authorName || '%'")
            params = {'productId': productId, 'authorName': request.args.get('authorName')}
        elif request.args.get('contentValue'):
            sql_query = text("SELECT * FROM review WHERE productId = :productId AND content LIKE '%' || :contentValue || '%'")
            params = {'productId': productId, 'contentValue': request.args.get('contentValue')}
        elif request.args.get('purchasedDateFrom') and request.args.get('purchasedDateTo'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId AND itemPurchased >= :purchasedDateFrom AND itemPurchased <= :purchasedDateTo')
            params = {'productId': productId, 'purchasedDateFrom': request.args.get('purchasedDateFrom'), 'purchasedDateTo': request.args.get('purchasedDateTo')}
        elif request.args.get('reviewDateFrom') and request.args.get('reviewDateTo'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId AND reviewAdded >= :reviewDateFrom AND reviewAdded <= :reviewDateTo')
            params = {'productId': productId, 'reviewDateFrom': request.args.get('reviewDateFrom'), 'reviewDateTo': request.args.get('reviewDateTo')}
        elif request.args.get('isPurchased'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId AND purchased = :isPurchased')
            params = {'productId': productId, 'isPurchased': request.args.get('isPurchased')}
        elif request.args.get('usefulReviewFrom') and request.args.get('usefulReviewTo'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId AND usefulReview >= :usefulReviewFrom AND usefulReview <= :usefulReviewTo')
            params = {'productId': productId, 'usefulReviewFrom': request.args.get('usefulReviewFrom'), 'usefulReviewTo': request.args.get('usefulReviewTo')}
        elif request.args.get('uselessReviewFrom') and request.args.get('uselessReviewTo'):
            sql_query = text('SELECT * FROM review WHERE productId = :productId AND uselessReview >= :uselessReviewFrom AND uselessReview <= :uselessReviewTo')
            params = {'productId': productId, 'uselessReviewFrom': request.args.get('uselessReviewFrom'), 'uselessReviewTo': request.args.get('uselessReviewTo')}
        else:
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

    @staticmethod
    def getStarsCountForReviews(productName):
        from app import db
        from sqlalchemy import text
        sql = """
        SELECT
            SUM(CASE WHEN stars = '1' THEN 1 ELSE 0 END) AS one_star_reviews,
            SUM(CASE WHEN stars = '1,5' THEN 1 ELSE 0 END) AS one_half_star_reviews,
            SUM(CASE WHEN stars = '2' THEN 1 ELSE 0 END) AS two_star_reviews,
            SUM(CASE WHEN stars = '2,5' THEN 1 ELSE 0 END) AS two_half_star_reviews,
            SUM(CASE WHEN stars = '3' THEN 1 ELSE 0 END) AS three_star_reviews,
            SUM(CASE WHEN stars = '3,5' THEN 1 ELSE 0 END) AS three_half_star_reviews,
            SUM(CASE WHEN stars = '4' THEN 1 ELSE 0 END) AS four_star_reviews,
            SUM(CASE WHEN stars = '4,5' THEN 1 ELSE 0 END) AS four_half_star_reviews,
            SUM(CASE WHEN stars = '5' THEN 1 ELSE 0 END) AS five_star_reviews
        FROM Review
        JOIN 
            Product ON Review.productId = Product.id
        WHERE 
         Product.title = :productName;
        """
        sql_query = text(sql)
        params = {'productName': productName}
        result = db.session.execute(sql_query, params)
        return [dict(zip(result.keys(), row)) for row in result.fetchall()][0]
    @staticmethod
    def getDataForDoughnutChart(productName):
        from app import db
        from sqlalchemy import text
        sql = """
        SELECT
                SUM(CASE WHEN recommended = true THEN 1 ELSE 0 END) AS true_count,
                SUM(CASE WHEN recommended = false and recommended != null THEN 1 ELSE 0 END) AS false_count
        FROM Review
        JOIN 
            Product ON Review.productId = Product.id
        WHERE 
         Product.title = :productName;
        """
        sql_query = text(sql)
        params = {'productName': productName}
        result = db.session.execute(sql_query, params)
        return [dict(zip(result.keys(), row)) for row in result.fetchall()][0]

