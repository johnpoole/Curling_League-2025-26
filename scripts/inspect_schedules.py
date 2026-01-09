import pdfplumber
import json
import re

def extract_schedule_manual(pdf_path, league_name):
    """Manual extraction with visual inspection"""
    games = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"\n{'='*80}")
        print(f"Processing: {league_name}")
        print('='*80)
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n--- Page {page_num} ---")
            
            # Extract tables
            tables = page.extract_tables()
            
            for table_num, table in enumerate(tables):
                if not table:
                    continue
                
                print(f"\nTable {table_num + 1}:")
                
                # Look for rows containing "Poole"
                for row_idx, row in enumerate(table):
                    if any(cell and 'poole' in str(cell).lower() for cell in row):
                        print(f"\nFound Poole in row {row_idx}:")
                        print(f"Row content: {row}")
                        
                        # Print surrounding rows for context
                        if row_idx > 0:
                            print(f"Previous row: {table[row_idx - 1]}")
                        if row_idx < len(table) - 1:
                            print(f"Next row: {table[row_idx + 1]}")
    
    return games

# Process both PDFs
monday_pdf = r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Monday Night Mens 2025 2026 28 1st Round - 28 teams.pdf"
tuesday_pdf = r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Tuesday Night Mens 2025 2026 1st Round 26 teams.pdf"

print("\n" + "="*80)
print("EXTRACTING SCHEDULE DATA - VISUAL INSPECTION")
print("="*80)

extract_schedule_manual(monday_pdf, "Monday Night")
extract_schedule_manual(tuesday_pdf, "Tuesday Night")

print("\n" + "="*80)
print("Please review the output above to verify opponent names")
print("="*80)
