from flask import Blueprint, render_template

appRoutes = Blueprint('appRoutes', __name__)


@appRoutes.route('/')
def homePage():
    return render_template('pages/home.html')
