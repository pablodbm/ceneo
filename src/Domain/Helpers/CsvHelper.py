from flask_csv import send_csv


class CsvHelper:
    @staticmethod
    def getCsvFile(data):
        return send_csv(data,"test.csv", ["id", "productId","author","content","stars","purchased","reviewAdded","itemPurchased","usefulReview","uselessReview","dataReviewId"])
