from flask import Blueprint, render_template

# Tworzenie obiektu Blueprint
AuthorRoutes = Blueprint('AuthorRoutes', __name__)


# Definiowanie trasy
@AuthorRoutes.route('/author')
def author():
    return render_template('pages/author.html')
