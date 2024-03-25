from flask import Blueprint, render_template

# Tworzenie obiektu Blueprint
appRoutes = Blueprint('appRoutes', __name__)


# Definiowanie trasy
@appRoutes.route('/')
def homePage():
    return render_template('index.html')
