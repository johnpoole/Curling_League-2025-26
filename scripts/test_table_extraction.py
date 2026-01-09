import pdfplumber

pdf = pdfplumber.open('Friday Night Mixed 2025 2026 1st Round 26 teams.pdf')
page = pdf.pages[0]

tables = page.extract_tables()
print(f"Found {len(tables)} tables\n")

if tables:
    print("First table (first 5 rows):")
    for i, row in enumerate(tables[0][:5]):
        print(f"Row {i}: {row}")
else:
    print("No tables found - falling back to text extraction")
