from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from statistics import mean
from datetime import date
from typing import Optional
import os

# Inițializăm aplicația
app = FastAPI(
    title="Report Generation Service",
    description="A backend service for generating reports in PDF and Excel formats.",
    version="1.0.0",
    contact={
        "name": "Druid45ra",
        "url": "https://github.com/Druid45ra/App-serviciu-generare-rapoarte",
        "email": "radu_vanca@live.com",
    },
)


# Modelul datelor de intrare
class DataModel(BaseModel):
    name: str
    value: float
    category: str


# Endpoint de test
@app.get(
    "/",
    summary="Service Status",
    description="Checks if the report generation service is running.",
)
async def root():
    return {"message": "Serviciul de generare rapoarte funcționează!"}


# Endpoint pentru upload de date
@app.post(
    "/upload-data/",
    summary="Upload Data",
    description="Uploads data for further processing.",
    response_description="Confirmation of the received data.",
)
async def upload_data(data: List[DataModel]):
    """
    Accepts a list of data entries for further processing.
    - **name**: Name of the data entry.
    - **value**: Numeric value associated with the entry.
    - **category**: Category to which the entry belongs.
    """
    return {"message": "Datele au fost primite!", "data": data}


# Endpoint pentru procesarea datelor
@app.post(
    "/process-data/",
    summary="Process Data",
    description="Processes the uploaded data and generates a summary.",
    response_description="Summary of processed data, including statistics.",
)
async def process_data(data: List[DataModel]):
    total_value = sum(item.value for item in data)
    average_value = mean(item.value for item in data)
    category_summary = {}
    for item in data:
        category_summary.setdefault(item.category, []).append(item.value)

    summary = {
        "total_value": total_value,
        "average_value": average_value,
        "category_summary": {
            category: {
                "total": sum(values),
                "average": mean(values),
                "count": len(values),
            }
            for category, values in category_summary.items()
        },
    }

    return {"message": "Datele au fost procesate!", "summary": summary}


# Endpoint pentru generarea raportului PDF
@app.post(
    "/generate-pdf/",
    summary="Generate PDF Report",
    description="Generates a PDF report based on the processed data.",
    response_description="PDF file for download.",
)
async def generate_pdf(data: List[DataModel]):
    total_value = sum(item.value for item in data)
    average_value = mean(item.value for item in data)
    category_summary = {}
    for item in data:
        category_summary.setdefault(item.category, []).append(item.value)

    pdf_file = "raport.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, "Raport - Serviciu de Generare Rapoarte")
    c.drawString(30, 730, f"Total Valoare: {total_value}")
    c.drawString(30, 710, f"Valoare Medie: {average_value:.2f}")

    y_position = 690
    for category, values in category_summary.items():
        c.drawString(30, y_position, f"Categoria: {category}")
        y_position -= 20
        c.drawString(50, y_position, f"  Total: {sum(values):.2f}")
        y_position -= 20
        c.drawString(50, y_position, f"  Media: {mean(values):.2f}")
        y_position -= 20
        c.drawString(50, y_position, f"  Elemente: {len(values)}")
        y_position -= 30

    c.save()
    return FileResponse(pdf_file, media_type="application/pdf", filename=pdf_file)


# Endpoint pentru generarea raportului Excel
@app.post(
    "/generate-excel/",
    summary="Generate Excel Report",
    description="Generates an Excel report based on the processed data.",
    response_description="Excel file for download.",
)
async def generate_excel(data: List[DataModel]):
    total_value = sum(item.value for item in data)
    average_value = mean(item.value for item in data)
    category_summary = {}
    for item in data:
        category_summary.setdefault(item.category, []).append(item.value)

    wb = Workbook()
    ws = wb.active
    ws.title = "Raport"
    ws.append(["Raport - Serviciu de Generare Rapoarte"])
    ws.append([])
    ws.append(["Total Valoare", total_value])
    ws.append(["Valoare Medie", average_value])
    ws.append([])
    ws.append(["Categorie", "Total", "Media", "Număr Elemente"])
    for category, values in category_summary.items():
        ws.append([category, sum(values), mean(values), len(values)])

    excel_file = "raport.xlsx"
    wb.save(excel_file)
    return FileResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=excel_file,
    )

    # Extindem modelul pentru datele de intrare cu câmpuri opționale de dată


class FilterCriteria(BaseModel):
    category: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


@app.post(
    "/filter-data/",
    summary="Filter Data",
    description="Filters the uploaded data based on specified criteria.",
    response_description="Filtered data based on the criteria.",
)
async def filter_data(data: List[DataModel], filters: FilterCriteria):
    """
    Filtrează datele pe baza următoarelor criterii:
    - **category**: Filtrare după categorie.
    - **min_value**: Valoare minimă permisă.
    - **max_value**: Valoare maximă permisă.
    """
    filtered_data = data

    if filters.category:
        filtered_data = [
            item for item in filtered_data if item.category == filters.category
        ]
    if filters.min_value is not None:
        filtered_data = [
            item for item in filtered_data if item.value >= filters.min_value
        ]
    if filters.max_value is not None:
        filtered_data = [
            item for item in filtered_data if item.value <= filters.max_value
        ]

    return {"message": "Datele au fost filtrate!", "filtered_data": filtered_data}


class ReportCustomization(BaseModel):
    include_name: bool = True
    include_value: bool = True
    include_category: bool = True


@app.post(
    "/generate-custom-pdf/",
    summary="Generate Custom PDF Report",
    description="Generates a PDF report based on selected fields.",
    response_description="Customized PDF file for download.",
)
async def generate_custom_pdf(
    data: List[DataModel], customization: ReportCustomization
):
    """
    Permite personalizarea raportului PDF.
    - **include_name**: Include câmpul `name` în raport.
    - **include_value**: Include câmpul `value` în raport.
    - **include_category**: Include câmpul `category` în raport.
    """
    pdf_file = "custom_raport.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, "Raport Personalizat - Serviciu de Generare Rapoarte")

    y_position = 730
    for item in data:
        if customization.include_name:
            c.drawString(30, y_position, f"Name: {item.name}")
            y_position -= 20
        if customization.include_value:
            c.drawString(30, y_position, f"Value: {item.value}")
            y_position -= 20
        if customization.include_category:
            c.drawString(30, y_position, f"Category: {item.category}")
            y_position -= 20
        y_position -= 10

    c.save()
    return FileResponse(pdf_file, media_type="application/pdf", filename=pdf_file)


import csv


@app.post(
    "/generate-csv/",
    summary="Generate CSV Report",
    description="Generates a CSV report based on the data.",
    response_description="CSV file for download.",
)
async def generate_csv(data: List[DataModel]):
    """
    Generează un raport CSV bazat pe datele primite.
    """
    csv_file = "raport.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Value", "Category"])
        for item in data:
            writer.writerow([item.name, item.value, item.category])

    return FileResponse(csv_file, media_type="text/csv", filename=csv_file)


@app.post(
    "/generate-json/",
    summary="Generate JSON Report",
    description="Generates a JSON report based on the data.",
    response_description="JSON data as response.",
)
async def generate_json(data: List[DataModel]):
    """
    Returnează datele primite în format JSON.
    """
    return {"message": "Raport generat în JSON", "data": data}
