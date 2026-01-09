import openpyxl

# Load the Excel file
wb = openpyxl.load_workbook('2025 2026 Curling Roster All Leagues (1).xlsx')
sheet = wb['Mixed']

print("First 30 rows of Mixed sheet:\n")
for row_idx, row in enumerate(sheet.iter_rows(values_only=True), 1):
    if row_idx <= 30:
        # Print all non-empty cells
        cells = [str(c) if c else '' for c in row[:10]]
        if any(cells):
            print(f"Row {row_idx}: {cells}")
