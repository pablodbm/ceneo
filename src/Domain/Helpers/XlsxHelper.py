from flask import Flask, make_response
import xlwt
import io

class XlsxHelper:
    @staticmethod
    def getXlsxFile(data):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Sheet1')
        headers = ["id", "productId", "author", "content", "stars", "purchased", "reviewAdded", "itemPurchased", "usefulReview",
         "uselessReview", "dataReviewId", "recommended"]
        for i in range(0,len(headers)):
            sheet.write(0, i, headers[i])
        for i in range(0,len(data)):
            for j in range(0,len(headers)):
                sheet.write(i+1, j, data[i][headers[j]])
        excel_data = io.BytesIO()
        workbook.save(excel_data)
        excel_data.seek(0)

        response = make_response(excel_data.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=example.xls"
        response.headers["Content-type"] = "application/vnd.ms-excel"
        return response