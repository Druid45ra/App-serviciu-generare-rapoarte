# App-serviciu-generare-rapoarte
Report Generation Service (PDF &amp; Excel)  This project is a backend service developed with FastAPI that allows the generation of reports in PDF and Excel formats. It processes input data (e.g., in JSON format), calculates summary statistics (like total value and average), and generates downloadable reports.

Report Generation Service (PDF & Excel)

This project is a backend service developed with FastAPI that allows the generation of reports in PDF and Excel formats. It processes input data (e.g., in JSON format), calculates summary statistics (like total value and average), and generates downloadable reports.
Features:

    Generate PDF Reports: Creates a PDF document containing summarized data with categories, totals, averages, and number of items.
    Generate Excel Reports: Outputs an Excel file with data structured into rows and columns, including statistics like totals, averages, and item counts per category.
    FastAPI Backend: Lightweight, fast, and easy-to-use framework for serving the report generation endpoints.
    OpenPyXL & ReportLab: Utilized libraries for generating Excel and PDF reports, respectively.

Technologies Used:

    FastAPI: A modern Python framework for building APIs.
    ReportLab: Library used to create PDF files.
    OpenPyXL: Library used for handling Excel files.
    Pandas: For data processing.

Setup:

    Clone this repository:

git clone https://github.com/Druid45ra/App-serviciu-generare-rapoarte.git

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the FastAPI server:

    uvicorn main:app --reload

Usage:

    POST /generate-pdf/: Generate a PDF report with provided data.
    POST /generate-excel/: Generate an Excel report with provided data.

