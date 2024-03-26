from flask import Blueprint, render_template, jsonify, Response

from src.Domain.Helpers import XlsxHelper
from src.Domain.Helpers.CsvHelper import CsvHelper
from src.Insfrastructure.Repositories.ProductRepository import productRepository
from src.Insfrastructure.Repositories.ReviewRepository import ReviewRepository
from src.Domain.Helpers.JsonHelper import JsonHelper

ProductRoutes = Blueprint('ProductRoutes', __name__)


@ProductRoutes.route('/product/<id>')
def product(id):
    params = productRepository.query(id)
    print(params)
    if params is None:
        return "nie ma takiego produktu"
    return render_template('pages/product.html',data=params)
@ProductRoutes.route('/products')
def products():
    params = productRepository.getAllProducts()
    return render_template("pages/products.html", products=params)

@ProductRoutes.route('/product/<productId>/<type>')
def generateFile(productId, type):
    data = ReviewRepository.getReviewsForProductId(productId)
    # return data
    if type == 'json':
        return JsonHelper.getJsonFile(data)
    elif type == 'csv':
        return CsvHelper.getCsvFile(data)
    elif type =='xlsx':
        return XlsxHelper.getXlsxFile(data)
    return productId + " " + type
