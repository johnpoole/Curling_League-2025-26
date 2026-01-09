import pdfplumber
import pandas as pd
import json
import re

def extract_tables_from_pdf(pdf_path):
    """Extract tables from PDF using pdfplumber's table extraction"""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            if tables:
                print(f"\n=== Page {page_num} - Found {len(tables)} table(s) ===")
                for table_idx, table in enumerate(tables):
                    print(f"\nTable {table_idx + 1}:")
                    if table:
                        for row_idx, row in enumerate(table[:10]):  # Print first 10 rows
                            print(f"  Row {row_idx}: {row}")
                        all_tables.append({
                            'page': page_num,
                            'table_idx': table_idx,
                            'data': table
                        })
    
    return all_tables

def find_poole_in_tables(tables, league_name):
    """Find all Poole games in extracted tables"""
    games = []
    
    for table_info in tables:
        table = table_info['data']
        page = table_info['page']
        
        # Look for date, sheet structure
        current_date = None
        current_time = None
        
        for row_idx, row in enumerate(table):
            if not row:
                continue
            
            # Check if this row has a date in first column
            if row[0]:
                date_match = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', str(row[0]))
                if date_match:
                    current_date = row[0].strip()
                    continue
            
            # Check if this row has a time in first column
            if row[0]:
                time_match = re.match(r'(\d+):(\d+)(am|pm)', str(row[0]))
                if time_match:
                    current_time = row[0].strip()
            
            # Search for Poole in this row
            if current_date and current_time:
                for col_idx, cell in enumerate(row):
                    if cell and 'poole' in str(cell).lower():
                        # Found Poole! col_idx tells us the sheet
                        # The opponent might be in adjacent cells in the same column
                        sheet_num = col_idx
                        
                        # Try to find opponent
                        opponent = "Unknown"
                        # Look in same column, previous row
                        if row_idx > 0 and table[row_idx - 1][col_idx]:
                            potential_opponent = str(table[row_idx - 1][col_idx]).strip()
                            if potential_opponent and potential_opponent.lower() != 'poole':
                                opponent = potential_opponent
                        
                        games.append({
                            'date': current_date,
                            'time': current_time,
                            'sheet': sheet_num,
                            'opponent': opponent,
                            'league': league_name,
                            'page': page,
                            'raw_row': row
                        })
    
    return games

print("=" * 80)
print("EXTRACTING TABLES FROM PDFs")
print("=" * 80)

print("\n### MONDAY NIGHT PDF ###")
monday_tables = extract_tables_from_pdf(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Monday Night Mens 2025 2026 28 1st Round - 28 teams.pdf"
)

print("\n\n### TUESDAY NIGHT PDF ###")
tuesday_tables = extract_tables_from_pdf(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Tuesday Night Mens 2025 2026 1st Round 26 teams.pdf"
)

print("\n\n" + "=" * 80)
print("FINDING POOLE GAMES")
print("=" * 80)

monday_games = find_poole_in_tables(monday_tables, "Monday Night")
print(f"\nMonday games found: {len(monday_games)}")
for game in monday_games:
    print(f"  {game['date']} {game['time']} Sheet {game['sheet']} vs {game['opponent']}")

tuesday_games = find_poole_in_tables(tuesday_tables, "Tuesday Night")
print(f"\nTuesday games found: {len(tuesday_games)}")
for game in tuesday_games:
    print(f"  {game['date']} {game['time']} Sheet {game['sheet']} vs {game['opponent']}")
