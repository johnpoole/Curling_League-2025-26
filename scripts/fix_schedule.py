import pdfplumber
import json
import re

def extract_schedule_correct(pdf_path, league_name):
    """Extract schedule with correct vertical opponent matching"""
    games = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            
            for table in tables:
                if not table:
                    continue
                
                current_date = None
                current_time = None
                
                for row_idx, row in enumerate(table):
                    if not row:
                        continue
                    
                    # Check for date in ANY column of this row
                    for cell in row:
                        if cell:
                            date_match = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', str(cell).strip())
                            if date_match:
                                current_date = str(cell).strip()
                                break
                    
                    # Check for time in ANY column of this row
                    for cell in row:
                        if cell:
                            time_match = re.match(r'(\d+):(\d+)(am|pm)', str(cell).strip())
                            if time_match:
                                current_time = str(cell).strip()
                                break
                    
                    # Search for Poole in this row
                    for col_idx, cell in enumerate(row):
                        if cell and 'poole' in str(cell).lower() and col_idx > 0:
                            print(f"Found Poole at row {row_idx}, col {col_idx}, date={current_date}, time={current_time}")
                            # Calculate sheet number based on column
                            # Columns: 0=Date/Time, then groups of 3 for each sheet
                            # Sheet 1: cols 3,4,5; Sheet 2: cols 6,7,8; etc
                            if col_idx >= 3:
                                sheet_num = ((col_idx - 3) // 3) + 1
                                
                                # Check both previous and next rows for opponent
                                opponent = "Unknown"
                                
                                # Try previous row first (opponent above)
                                if row_idx > 0:
                                    prev_row = table[row_idx - 1]
                                    if col_idx < len(prev_row) and prev_row[col_idx]:
                                        potential_opponent = str(prev_row[col_idx]).strip()
                                        # Check if it's a valid team name (not date, time, or empty)
                                        if (potential_opponent and 
                                            potential_opponent != 'None' and 
                                            '@' not in potential_opponent and
                                            not re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', potential_opponent) and
                                            not re.match(r'\d+:\d+(am|pm)', potential_opponent) and
                                            'Sheet' not in potential_opponent):
                                            opponent = potential_opponent
                                
                                # If not found above, try next row (opponent below)
                                if opponent == "Unknown" and row_idx + 1 < len(table):
                                    next_row = table[row_idx + 1]
                                    if col_idx < len(next_row) and next_row[col_idx]:
                                        potential_opponent = str(next_row[col_idx]).strip()
                                        if (potential_opponent and 
                                            potential_opponent != 'None' and 
                                            '@' not in potential_opponent and
                                            not re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', potential_opponent) and
                                            not re.match(r'\d+:\d+(am|pm)', potential_opponent) and
                                            'Sheet' not in potential_opponent):
                                            opponent = potential_opponent
                                
                                # Only add if we have date, time, and a valid opponent
                                if current_date and current_time and opponent != "Unknown":
                                    games.append({
                                        'date': current_date,
                                        'time': current_time,
                                        'sheet': sheet_num,
                                        'opponent': opponent,
                                        'league': league_name
                                    })
    
    return games

# Extract schedules
print("Extracting Monday Night schedule...")
monday_games = extract_schedule_correct(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Monday Night Mens 2025 2026 28 1st Round - 28 teams.pdf",
    "Monday Night"
)

print("Extracting Tuesday Night schedule...")
tuesday_games = extract_schedule_correct(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Tuesday Night Mens 2025 2026 1st Round 26 teams.pdf",
    "Tuesday Night"
)

# Load existing data to preserve rosters
with open('poole_team_data.json', 'r') as f:
    poole_data = json.load(f)

# Update only the schedule
poole_data["schedule"] = monday_games + tuesday_games

# Save
with open('poole_team_data.json', 'w', encoding='utf-8') as f:
    json.dump(poole_data, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("UPDATED SCHEDULE")
print("="*80)
print(f"Monday Night: {len(monday_games)} games")
for game in monday_games:
    print(f"  {game['date']:>10} | {game['time']:>7} | Sheet {game['sheet']} | vs {game['opponent']}")

print(f"\nTuesday Night: {len(tuesday_games)} games")
for game in tuesday_games:
    print(f"  {game['date']:>10} | {game['time']:>7} | Sheet {game['sheet']} | vs {game['opponent']}")

print("\n* Schedule updated in poole_team_data.json")
