import openpyxl

# Load the Excel file
wb = openpyxl.load_workbook('2025 2026 Curling Roster All Leagues (1).xlsx')

print("Available sheets:")
for sheet_name in wb.sheetnames:
    print(f"  - {sheet_name}")
