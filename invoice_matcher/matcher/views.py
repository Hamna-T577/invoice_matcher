from django.shortcuts import render
from django.http import HttpResponse
import pytesseract
import pdfplumber
import os
import tempfile
import re

import os
os.environ["PATH"] += os.pathsep + r"C:\poppler\Library\bin"




# 👇 Configure Tesseract path if needed

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def upload_view(request):
    if request.method == "POST":
        invoices = request.FILES.getlist("invoices")
        pos = request.FILES.getlist("pos")

        matches = []

        for inv_file in invoices:
            # Save invoice file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                for chunk in inv_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            inv_data = extract_info_from_pdf(tmp_path)
            os.remove(tmp_path)

            # Compare with each PO
            for po_file in pos:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    for chunk in po_file.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name

                po_data = extract_info_from_pdf(tmp_path)
                os.remove(tmp_path)

                # ---- Match Logic ----
                inv_total = normalize_total(inv_data["total"])
                po_total = normalize_total(po_data["total"])

                # Debug info in console
                print(f"\n🔍 Comparing {inv_file.name} vs {po_file.name}")
                print(f"Invoice total: {inv_total}, PO total: {po_total}")

                # Compare totals and vendor
                if inv_total is not None and po_total is not None:
                    total_match = abs(inv_total - po_total) < 0.01
                    vendor_match = (
                        inv_data["vendor"]
                        and po_data["vendor"]
                        and inv_data["vendor"].lower() in po_data["vendor"].lower()
                    )

                    if total_match and vendor_match:
                        status = "MATCH ✅"
                    elif total_match:
                        status = "PARTIAL MATCH ⚠️ (Total matched, vendor differs)"
                    else:
                        status = "MISMATCH ⚠️"
                else:
                    status = "MISSING VALUE ⚠️"

                messages = [
                    f"Invoice Total: {inv_data['total'] or 'N/A'}",
                    f"PO Total: {po_data['total'] or 'N/A'}",
                    f"Vendor: {inv_data['vendor'] or 'N/A'} vs {po_data['vendor'] or 'N/A'}",
                ]

                matches.append({
                    "invoice_name": inv_file.name,
                    "po_name": po_file.name,
                    "status": status,
                    "messages": messages
                })

        return render(request, "matcher/results.html", {"matches": matches})

    return render(request, "matcher/upload.html")





def extract_info_from_pdf(file):
    """Extract invoice/PO number, vendor, total, and items (supports OCR)."""
    import pytesseract
    from pdf2image import convert_from_path
    import pdfplumber

    text = ""

    # 1️⃣ Try extracting normal text
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"

    # 2️⃣ If no text found, use OCR (for scanned images)
    if not text.strip():
        print("📄 OCR Extracted Text Preview:\n", text[:1000])

        print("⚙️ Using OCR for image-based PDF...")
        pages = convert_from_path(file)
        for page in pages:
            text += pytesseract.image_to_string(page)

    # 3️⃣ Extract key info
    info = {
        "number": None,
        "vendor": None,
        "total": None,
        "items": [],
    }

    number_match = re.search(r'(INV|PO)[\-\s:]*(\d+)', text, re.I)
    if number_match:
        info["number"] = number_match.group(0).strip()

    vendor_match = re.search(r'Vendor\s*[:\-]?\s*(.+)', text, re.I)
    if vendor_match:
        info["vendor"] = vendor_match.group(1).splitlines()[0].strip()


    total_match = re.search(r'Tot[a|o|0|l|i]{2,}\s*[:\-]?\s*\$?([\d,]+\.\d{1,2})', text, re.I)

    if total_match:
        info["total"] = total_match.group(1).strip()

    # Extract item lines with prices
    for line in text.splitlines():
        if "$" in line:
            info["items"].append(line.strip())

    return info






def normalize_total(value):
    """Clean and convert extracted totals to float safely."""
    if not value:
        return None
    value = re.sub(r"[^\d.]", "", value)  # remove $ and commas
    try:
        return float(value)
    except ValueError:
        return None


# ✅ Simple check route
def check_view(request):
    return HttpResponse("<h1>Invoice Matcher is working! 🚀</h1>")
