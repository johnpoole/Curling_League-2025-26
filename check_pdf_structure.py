import pdfplumber

pdf = pdfplumber.open('Friday Night Mixed 2025 2026 1st Round 26 teams.pdf')
lines = pdf.pages[0].extract_text().split('\n')

print("PDF Structure - First 15 lines:\n")
for i, line in enumerate(lines[:15], 1):
    print(f"{i:2d}: {line}")
