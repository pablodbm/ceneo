from flask import Blueprint, render_template, request

from src.Domain.Helpers.XlsxHelper import XlsxHelper
from src.Domain.Helpers.CsvHelper import CsvHelper
from src.Insfrastructure.Repositories.ProductRepository import productRepository
from src.Insfrastructure.Repositories.ReviewRepository import ReviewRepository
from src.Domain.Helpers.JsonHelper import JsonHelper

ProductRoutes = Blueprint('ProductRoutes', __name__)


@ProductRoutes.route('/product/<id>')
def product(id):
    params = productRepository.query(id, request)
    if params is None:
        return "nie ma takiego produktu"
    return render_template('pages/product.html',data=params, sortBy=request.args.get('sortBy'), orderBy=request.args.get('orderBy'))
@ProductRoutes.route('/products')
def products():
    params = productRepository.getAllProducts()
    return render_template("pages/products.html", products=params)

@ProductRoutes.route('/product/<productId>/<type>')
def generateFile(productId, type):
    data = ReviewRepository.getReviewsForProductId(productId)
    if type == 'json':
        return JsonHelper.getJsonFile(data)
    elif type == 'csv':
        return CsvHelper.getCsvFile(data)
    elif type =='xlsx':
        return XlsxHelper.getXlsxFile(data)
    return productId + " " + type

@ProductRoutes.route('/product/charts/<productName>')
def generateChart(productName):
    barChart = ReviewRepository.getStarsCountForReviews(productName)
    DoughnutChart = ReviewRepository.getDataForDoughnutChart(productName)
    return render_template("pages/productCharts.html", productName=productName, barChart=barChart, DoughnutChart=DoughnutChart)
