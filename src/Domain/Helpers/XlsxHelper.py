from flask import Flask, request, jsonify
from flask import excel


class XlsxHelper:
    @staticmethod
    def getXlsxFile(data):
        return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                              file_name="export_data")
