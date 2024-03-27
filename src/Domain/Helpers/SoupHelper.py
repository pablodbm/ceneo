from bs4 import BeautifulSoup
import uuid, requests
from src.Domain.ProsAndCons.ProsAndConsEnum import ProsAndConsEnum
class SoupHelper:
    url = "https://www.ceneo.pl/"

    @staticmethod
    def getSoup(url, id):
        response = requests.get(url+id)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None

    @staticmethod
    def getName(soup):
        return soup.find("h1", class_="product-top__product-info__name").text.replace("/"," ")

    @staticmethod
    def getReviewsCount(soup):
        content = soup.find('div', class_="score-extend__review")
        if content is None:
            return 0
        return soup.find('div', class_="score-extend__review").text.split(" ")[0]

    @staticmethod
    def getAvgMark(soup):
        return soup.find('div', class_="score-extend").find('div').find('font').text

    @staticmethod
    def getAllReviews(soup, productId):
        opinions = soup.find("div", class_="js_product-reviews js_reviews-hook js_product-reviews-container").find_all("div", class_="user-post user-post__card js_product-review")
        for opinion in opinions:
            reviewId = str(uuid.uuid4())
            SoupHelper.saveSingleReview(opinion,productId, reviewId, opinion.get('data-review-id'))


    def saveSingleReview(opinion, productId, reviewId, dataReviewId):
        from app import db, Review
        stars = SoupHelper.getStarsForReview(opinion)
        author = SoupHelper.getAuthorForReview(opinion)
        content = SoupHelper.getReviewContent(opinion)
        purchased = SoupHelper.isPurchased(opinion)
        reviewAdded = SoupHelper.getReviewAdded(opinion)
        itemPurchased = SoupHelper.getPurchasedTime(opinion)
        usefulReview = SoupHelper.getUsefulReview(opinion)
        uselessReview = SoupHelper.getUselessReview(opinion)
        recommended = SoupHelper.isRecommended(opinion)
        newReview = Review(id=reviewId, productId=productId, author=author,content=content, stars=stars,purchased=purchased, reviewAdded=reviewAdded, itemPurchased=itemPurchased, usefulReview=usefulReview, uselessReview=uselessReview, dataReviewId=dataReviewId, recommended=recommended)
        db.session.add(newReview)
        db.session.commit()

        SoupHelper.saveProsAndConsForReview(opinion, productId, reviewId)


    def getStarsForReview(soup):
        return soup.find("span", class_="user-post__score-count").text.split("/")[0]
    def getAuthorForReview(soup):
        return soup.find("span", class_="user-post__author-name").text.rstrip()
    def getReviewContent(soup):
        return soup.find("div", class_="user-post__text").text
    def isPurchased(soup):
        if soup.find("div", class_="review-pz") is not None:
            return True
        return False
    def getReviewAdded(soup):
        dates = soup.find("span", class_="user-post__published").find_all("time")
        try:
            return dates[0].get('datetime')
        except IndexError:
            return None
    def getPurchasedTime(soup):
        dates = soup.find("span", class_="user-post__published").find_all("time")
        try:
            return dates[1].get('datetime')
        except IndexError:
            return None
    def getUsefulReview(soup):
        return soup.find("button",class_="vote-yes js_product-review-vote js_vote-yes").get('data-total-vote')
    def getUselessReview(soup):
        return soup.find("button",class_="vote-no js_product-review-vote js_vote-no").get('data-total-vote')
    def isRecommended(soup):
        span = soup.find("span", class_="user-post__author-recomendation")
        if span == None:
            return None
        em = span.find("em")
        if em.get('class')[0] == 'recommended':
            return True
        else:
            return False




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


