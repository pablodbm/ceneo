
from flask import Blueprint, render_template, request, redirect
from src.Application.Product.Command.ExtractProduct import ExtractProduct
from src.Application.Product.Command.ExtractProductHandler import ExtractProductHandler

ExtractionRoutes = Blueprint('ExtractionRoutes', __name__)


@ExtractionRoutes.route('/extraction', methods=['GET'])
def extraction():
    return render_template('pages/extraction.html',error=request.args.get('error'))

@ExtractionRoutes.route('/extraction', methods=['POST'])
def extractionHandler():
    if 0 == len(request.form.get('product_id')):
        return redirect("/extraction?error=1")
    command = ExtractProduct(request.form.get('product_id'))
    productName = ExtractProductHandler.handle(command)
    if productName is None:
        return redirect("/extraction?error=1")
    return redirect("/product/"+productName)
