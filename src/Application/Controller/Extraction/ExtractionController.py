
from flask import Blueprint, render_template, request, redirect
from src.Application.Product.ExtractProduct import ExtractProduct
from src.Application.Product.ExtractProductHandler import ExtractProductHandler

# Tworzenie obiektu Blueprint
ExtractionRoutes = Blueprint('ExtractionRoutes', __name__)


# Definiowanie trasy
@ExtractionRoutes.route('/extraction', methods=['GET'])
def extraction():
    return render_template('pages/extraction.html',error=request.args.get('error'))

@ExtractionRoutes.route('/extraction', methods=['POST'])
def extractionHandler():
    if 0 == len(request.form.get('product_id')):
        return redirect("/extraction?error=1")
    command = ExtractProduct(request.form.get('product_id'))
    ExtractProductHandler.handle(command)
    return "klk"
