from flask import  Response
import json


class JsonHelper:
    @staticmethod
    def getJsonFile(data):
        response = Response(json.dumps(data), content_type='application/json')
        response.headers['Content-Disposition'] = 'attachment; filename=test.json'
        return response
