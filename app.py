from flask import Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from src.Application.Controller.App.AppController import appRoutes
from src.Application.Controller.Author.AuthorController import AuthorRoutes
from src.Application.Controller.Extraction.ExtractionController import ExtractionRoutes
from src.Application.Controller.Product.ProductController import ProductRoutes
from src.Insfrastructure.Models.Models import db, Product, Review, ProsAndCons


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{Path(__file__).parent / 'data.db'}"
db.init_app(app)

# Rejestrowanie Blueprint w aplikacji
app.register_blueprint(appRoutes)
app.register_blueprint(AuthorRoutes)
app.register_blueprint(ExtractionRoutes)
app.register_blueprint(ProductRoutes)

# if __name__ == '__main__':
with app.app_context():
    db.create_all()
app.run(debug=True)