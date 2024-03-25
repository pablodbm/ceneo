
from flask import Blueprint, render_template, request
from src.Application.Product.ExtractProduct import ExtractProduct
from src.Application.Product.ExtractProductHandler import ExtractProductHandler

# Tworzenie obiektu Blueprint
ExtractionRoutes = Blueprint('ExtractionRoutes', __name__)


# Definiowanie trasy
@ExtractionRoutes.route('/extraction', methods=['GET'])
def extraction():
    return render_template('pages/extraction.html')

@ExtractionRoutes.route('/extraction', methods=['POST'])
def extractionHandler():

    command = ExtractProduct(request.form.get('product_id'))
    ExtractProductHandler.handle(command)
    return "klk"
