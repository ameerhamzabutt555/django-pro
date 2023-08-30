from django.urls import path
from employee_salary_module.views import generatePDF, generateCSV, render_pdf_view

urlpatterns = [
    path("<int:id>/generatePDF/", generatePDF, name="generatePDF"),
    path("<int:id>/generateCSV", generateCSV, name="generateCSV"),
    path("render_pdf_view/<int:id>", render_pdf_view, name="render_pdf_view"),
]
