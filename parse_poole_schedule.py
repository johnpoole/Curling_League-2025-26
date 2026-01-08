import pdfplumber
import openpyxl
import pandas as pd
import json
import re
from datetime import datetime

def parse_schedule_page(text, league_name, year=2025):
    """Parse a schedule page and extract Poole games"""
    games = []
    lines = text.split('\n')
    
    current_date = None
    current_time = None
    
    for line in lines:
        # Look for date pattern (e.g., "Oct 6", "Nov 24", "Jan 5")
        date_match = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', line)
        if date_match:
            month_str = date_match.group(1)
            day = date_match.group(2)
            current_date = f"{month_str} {day}"
            
            # Look for time in the same line or next line
            time_match = re.search(r'(\d+):(\d+)(am|pm)', line)
            if time_match:
                current_time = f"{time_match.group(1)}:{time_match.group(2)}{time_match.group(3)}"
            continue
        
        # Look for time pattern on its own line
        time_match = re.match(r'(\d+):(\d+)(am|pm)', line.strip())
        if time_match:
            current_time = f"{time_match.group(1)}:{time_match.group(2)}{time_match.group(3)}"
            continue
        
        # Check if this line contains Poole
        if 'poole' in line.lower() and current_date and current_time:
            # Extract sheet number and opponent
            # Split the line by spaces to find Poole and surrounding teams
            parts = line.split()
            
            # Find Poole's position
            poole_idx = -1
            for i, part in enumerate(parts):
                if 'poole' in part.lower():
                    poole_idx = i
                    break
            
            if poole_idx >= 0:
                # Determine sheet number based on position in line
                # The teams are listed in pairs for each sheet (home vs away)
                sheet_num = (poole_idx // 2) + 1
                
                # Determine opponent (the other team in the pair)
                if poole_idx % 2 == 0:
                    # Poole is first in pair, opponent is next
                    opponent = parts[poole_idx + 1] if poole_idx + 1 < len(parts) else "Unknown"
                else:
                    # Poole is second in pair, opponent is previous
                    opponent = parts[poole_idx - 1] if poole_idx > 0 else "Unknown"
                
                # Clean up opponent name
                opponent = opponent.strip()
                
                games.append({
                    'date': current_date,
                    'time': current_time,
                    'sheet': sheet_num,
                    'opponent': opponent,
                    'league': league_name,
                    'raw_line': line.strip()
                })
    
    return games

def extract_all_poole_games(pdf_path, league_name):
    """Extract all Poole games from a PDF"""
    all_games = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and 'poole' in text.lower():
                games = parse_schedule_page(text, league_name)
                all_games.extend(games)
    
    return all_games

def extract_poole_roster():
    """Extract Poole team roster from Excel"""
    excel_path = r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\2025 2026 Curling Roster All Leagues (1).xlsx"
    
    # Monday roster
    monday_roster = {
        'league': 'Monday Night',
        'players': []
    }
    
    # Tuesday roster
    tuesday_roster = {
        'league': 'Tuesday Night',
        'players': []
    }
    
    # Read Monday sheet
    try:
        df_monday = pd.read_excel(excel_path, sheet_name='Monday Men\'s')
        for idx, row in df_monday.iterrows():
            row_text = ' '.join([str(val) for val in row.values if pd.notna(val)])
            if 'poole' in row_text.lower():
                # Extract names from this row
                for val in row.values:
                    val_str = str(val)
                    # Check if it looks like a name (has letters, not an email, not a number)
                    if pd.notna(val) and '@' not in val_str and not val_str.isdigit() and len(val_str) > 2:
                        if any(c.isalpha() for c in val_str):
                            monday_roster['players'].append(val_str.strip())
    except Exception as e:
        print(f"Error reading Monday sheet: {e}")
    
    # Read Tuesday sheet
    try:
        df_tuesday = pd.read_excel(excel_path, sheet_name='Tuesday Men\'s')
        for idx, row in df_tuesday.iterrows():
            row_text = ' '.join([str(val) for val in row.values if pd.notna(val)])
            if 'poole' in row_text.lower():
                # Extract names from this row
                for val in row.values:
                    val_str = str(val)
                    # Check if it looks like a name
                    if pd.notna(val) and '@' not in val_str and not val_str.isdigit() and len(val_str) > 2:
                        if any(c.isalpha() for c in val_str) and 'Pool' not in val_str:
                            tuesday_roster['players'].append(val_str.strip())
    except Exception as e:
        print(f"Error reading Tuesday sheet: {e}")
    
    return monday_roster, tuesday_roster

# Main execution
print("Extracting Poole schedule data...")

# Extract Monday games
monday_games = extract_all_poole_games(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Monday Night Mens 2025 2026 28 1st Round - 28 teams.pdf",
    "Monday Night"
)

# Extract Tuesday games
tuesday_games = extract_all_poole_games(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Tuesday Night Mens 2025 2026 1st Round 26 teams.pdf",
    "Tuesday Night"
)

# Extract rosters
monday_roster, tuesday_roster = extract_poole_roster()

# Combine all data
poole_data = {
    "team_name": "Poole",
    "leagues": [],
    "schedule": [],
    "rosters": []
}

# Add leagues
if monday_games:
    poole_data["leagues"].append("Monday Night")
if tuesday_games:
    poole_data["leagues"].append("Tuesday Night")

# Add all games
poole_data["schedule"] = monday_games + tuesday_games

# Add rosters
if monday_roster['players']:
    poole_data["rosters"].append(monday_roster)
if tuesday_roster['players']:
    poole_data["rosters"].append(tuesday_roster)

# Print summary
print(f"\nTeam: {poole_data['team_name']}")
print(f"Leagues: {', '.join(poole_data['leagues'])}")
print(f"\nTotal games found: {len(poole_data['schedule'])}")
print(f"  Monday: {len(monday_games)}")
print(f"  Tuesday: {len(tuesday_games)}")

print("\n=== SCHEDULE ===")
for game in poole_data['schedule']:
    print(f"{game['league']}: {game['date']} at {game['time']}, Sheet {game['sheet']} vs {game['opponent']}")

print("\n=== ROSTERS ===")
for roster in poole_data['rosters']:
    print(f"\n{roster['league']}:")
    for player in roster['players']:
        print(f"  - {player}")

# Save to JSON
with open('poole_data.json', 'w', encoding='utf-8') as f:
    json.dump(poole_data, f, indent=2, ensure_ascii=False)

print("\n✓ Data saved to poole_data.json")
