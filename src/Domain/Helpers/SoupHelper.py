from bs4 import BeautifulSoup
import uuid
from src.Domain.ProsAndCons.ProsAndConsEnum import ProsAndConsEnum
class SoupHelper:
    url = "https://www.ceneo.pl/"

    @staticmethod
    def getSoup(url, id):
        with open('exampleCeneoSite.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        return soup

    @staticmethod
    def getName(soup):
        return soup.find("h1", class_="product-top__product-info__name").text

    @staticmethod
    def getReviewsCount(soup):
        return soup.find('div', class_="score-extend__review").text.split(" ")[0]

    @staticmethod
    def getAvgMark(soup):
        return soup.find('div', class_="score-extend").find('div').find('font').text

    @staticmethod
    def getAllReviews(soup, productId):
        opinions = soup.find("div", class_="js_product-reviews js_reviews-hook js_product-reviews-container").find_all("div", class_="user-post user-post__card js_product-review")
        for opinion in opinions:
            reviewId = str(uuid.uuid4())
            SoupHelper.saveSingleReview(opinion,productId, reviewId)


    def saveSingleReview(opinion, productId, reviewId):
        from app import db, Review
        stars = SoupHelper.getStarsForReview(opinion)
        author = SoupHelper.getAuthorForReview(opinion)
        content = SoupHelper.getReviewContent(opinion)

        newReview = Review(id=reviewId, productId=productId, author=author,content=content, stars=stars)
        db.session.add(newReview)
        db.session.commit()

        SoupHelper.saveProsAndConsForReview(opinion, productId, reviewId)


    def getStarsForReview(soup):
        return soup.find("span", class_="user-post__score-count").text.split("/")[0]
    def getAuthorForReview(soup):
        return soup.find("span", class_="user-post__author-name").text.rstrip()
    def getReviewContent(soup):
        return soup.find("div", class_="user-post__text").text

    def saveProsAndConsForReview(soup, productId, reviewId):
        rows = soup.find_all("div", class_="review-feature")
        from app import db, ProsAndCons
        for row in rows:
            type = ''
            if row.find("div", class_="review-feature__title review-feature__title--negatives") is not None:
                type = ProsAndConsEnum.cons
            elif row.find("div", class_="review-feature__title review-feature__title--positives") is not None:
                type = ProsAndConsEnum.pros

            for item in row.find_all("div", class_="review-feature__item"):
                newProsAndCons = ProsAndCons(id=str(uuid.uuid4()),reviewId=reviewId, productId=productId, text=item.text, type=type)
                db.session.add(newProsAndCons)
                db.session.commit()


    def getTextForProsAndCons(soup):
        return

