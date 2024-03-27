from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    avgMark = db.Column(db.String(64), nullable=False)
    reviewsCount = db.Column(db.Double, nullable=True)
    prosCount = db.Column(db.Double, nullable=True)
    consCount = db.Column(db.Double, nullable=True)
class Review(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('product.id'))
    author = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    stars = db.Column(db.String(16), nullable=False)
    purchased = db.Column(db.Boolean, nullable=True, default=False)
    reviewAdded = db.Column(db.String(64), nullable=True)
    itemPurchased = db.Column(db.String(64), nullable=True)
    usefulReview = db.Column(db.Integer, nullable=True, default=0)
    uselessReview = db.Column(db.Integer, nullable=True, default=0)
    dataReviewId = db.Column(db.String(64), nullable=True)
    recommended = db.Column(db.Boolean, nullable=True, default=False)

class ProsAndCons(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    reviewId = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(4), nullable=False)
