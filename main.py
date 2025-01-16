from fastapi import FastAPI

# Inițializăm aplicația
app = FastAPI()

# Endpoint de test
@app.get("/")
async def root():
    return {"message": "Serviciul de generare rapoarte funcționează!"}

from pydantic import BaseModel
from typing import List, Dict

# Modelul datelor de intrare
class DataModel(BaseModel):
    name: str
    value: float
    category: str

# Endpoint pentru upload de date
@app.post("/upload-data/")
async def upload_data(data: List[DataModel]):
    # Procesăm datele primite (pentru acum doar le returnăm)
    return {"message": "Datele au fost primite!", "data": data}

# Importuri necesare
from statistics import mean

# Endpoint pentru procesarea datelor
@app.post("/process-data/")
async def process_data(data: List[DataModel]):
    # Calculăm statistici
    total_value = sum(item.value for item in data)
    average_value = mean(item.value for item in data)

    # Grupăm datele pe categorii
    category_summary = {}
    for item in data:
        if item.category not in category_summary:
            category_summary[item.category] = []
        category_summary[item.category].append(item.value)

    # Rezumat
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

from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Endpoint pentru generarea raportului PDF
@app.post("/generate-pdf/")
async def generate_pdf(data: List[DataModel]):
    # Procesăm datele
    total_value = sum(item.value for item in data)
    average_value = mean(item.value for item in data)

    # Grupăm datele pe categorii
    category_summary = {}
    for item in data:
        if item.category not in category_summary:
            category_summary[item.category] = []
        category_summary[item.category].append(item.value)

    # Calea fișierului PDF
    pdf_file = "raport.pdf"

    # Creăm PDF-ul
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

    # Închidem PDF-ul
    c.save()

    # Returnăm PDF-ul pentru descărcare
    return FileResponse(pdf_file, media_type='application/pdf', filename=pdf_file)

from openpyxl import Workbook

# Endpoint pentru generarea raportului Excel
@app.post("/generate-excel/")
async def generate_excel(data: List[DataModel]):
    # Procesăm datele
    total_value = sum(item.value for item in data)
    average_value = mean(item.value for item in data)

    # Grupăm datele pe categorii
    category_summary = {}
    for item in data:
        if item.category not in category_summary:
            category_summary[item.category] = []
        category_summary[item.category].append(item.value)

    # Creăm workbook-ul Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Raport"

    # Adăugăm titlu
    ws.append(["Raport - Serviciu de Generare Rapoarte"])
    ws.append([])

    # Adăugăm statistici generale
    ws.append(["Total Valoare", total_value])
    ws.append(["Valoare Medie", average_value])
    ws.append([])

    # Adăugăm statistici pe categorii
    ws.append(["Categorie", "Total", "Media", "Număr Elemente"])
    for category, values in category_summary.items():
        ws.append([
            category,
            sum(values),
            mean(values),
            len(values)
        ])

    # Salvăm fișierul Excel
    excel_file = "raport.xlsx"
    wb.save(excel_file)

    # Returnăm fișierul pentru descărcare
    return FileResponse(excel_file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=excel_file)

