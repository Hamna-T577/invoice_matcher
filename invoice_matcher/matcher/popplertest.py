from pdf2image import convert_from_path
import os

# Add poppler bin to PATH
os.environ["PATH"] += os.pathsep + r"C:\poppler\Library\bin"

pdf_path = r"C:\Users\admin\Downloads\horizontal-invoice.pdf"



try:
    pages = convert_from_path(pdf_path)
    print(f"✅ Poppler worked! Number of pages: {len(pages)}")
    # Save first page as image to check
    pages[0].save("page1_test.png", "PNG")
    print("First page saved as page1_test.png")
except Exception as e:
    print("Error:", e)
