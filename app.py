from flask import Flask
from src.Application.Controller.App.AppController import appRoutes
from src.Application.Controller.Author.AuthorController import AuthorRoutes
from src.Application.Controller.Extraction.ExtractionController import ExtractionRoutes

app = Flask(__name__)

# Rejestrowanie Blueprint w aplikacji
app.register_blueprint(appRoutes)
app.register_blueprint(AuthorRoutes)
app.register_blueprint(ExtractionRoutes)

if __name__ == '__main__':
    app.run(debug=True)