from flask import Blueprint, render_template

AuthorRoutes = Blueprint('AuthorRoutes', __name__)


@AuthorRoutes.route('/author')
def author():
    return render_template('pages/author.html')
