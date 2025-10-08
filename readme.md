# 🧾 Invoice Matcher Project

The **Invoice Matcher** is a Django-based web application that compares **Invoices** and **Purchase Orders (POs)** using **OCR (Tesseract)** and **PDF text extraction (PDFPlumber)**.  
It helps automatically check whether uploaded invoices and purchase orders match by reading their content.

---

## 🌟 Features

✅ Upload multiple Invoices and Purchase Orders  
✅ Extract text from both PDFs using **Tesseract OCR** and **PDFPlumber**  
✅ Automatically compare extracted data to find **matches or mismatches**  
✅ Beautiful and responsive interface using **HTML + CSS**  
✅ Easy to set up and run locally

---

## 🛠️ Requirements

Make sure you have the following installed on your system:

- **Python 3.10+**
- **Django 5.x**
- **Tesseract OCR**
- **Poppler** (for PDF processing)
- **pdfplumber** and **pytesseract** Python libraries
- **VS Code** (optional but recommended)

---

## ⚙️ Step-by-Step Setup Instructions

### 🧩 1. Clone or Download the Project

If you downloaded the project as a ZIP:
- Extract it anywhere (for example, Desktop)
- Open the folder in **VS Code**

Or if you have Git:
```bash
git clone https://github.com/<your-username>/InvoiceMatcherProject.git
cd InvoiceMatcherProject
