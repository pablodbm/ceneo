from flask import Blueprint, render_template

# Tworzenie obiektu Blueprint
ProductRoutes = Blueprint('ProductRoutes', __name__)


# Definiowanie trasy
@ProductRoutes.route('/product/<id>')
def product(id):
    return render_template('pages/extraction.html',product=id)
