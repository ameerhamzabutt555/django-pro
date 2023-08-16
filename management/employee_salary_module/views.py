from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.shortcuts import render
from django.http import HttpResponse
import csv


# Create your views here.
def generatePDF(request, id):
    # buffer = io.BytesIO()
    # x = canvas.Canvas(buffer)
    # x.drawString(100, 100, "Let's generate this pdf file.")
    # x.showPage()
    # x.save()
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename="attempt1.pdf")
    print("jflkjkdlfjkldsjflks", id)

    return render(request, "admin/person/file.html", {"clients": id})


import csv


def generateCSV(request, id):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment;filename="example.csv"'},
    )

    csvv = csv.writer(response)
    csvv.writerow(["Diana", "has", "a", "police", "case"])
    csvv.writerow(["Let", "us", "get", "her", "a", "lawyer"])
    csvv.writerow(["shall", "we", "now"])

    return response


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from employee_salary_module.models import Employee, Salary


def render_pdf_view(request, id):
    salary = Salary.objects.get(pk=id)
    print("tgdsgnlkdgjdj", salary)
    full_name = salary.employee.first_name + " " + salary.employee.last_name
    total = (
        float(salary.employee.monthly_income)
        + salary.employee.allowance
        + salary.employee.medical
        + salary.employee.mobile_bils
    )
    template_path = "employee_salary_module/salary_pdf.html"
    context = {"salary": salary, "full_name": full_name, "total": total}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response
