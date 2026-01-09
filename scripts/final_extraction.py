import pdfplumber
import json
import re

def parse_schedule_tables(pdf_path, league_name):
    """Parse schedule from PDF tables"""
    games = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            
            for table in tables:
                if not table:
                    continue
                
                # Process table rows
                current_date = None
                current_time = None
                
                for row_idx, row in enumerate(table):
                    if not row:
                        continue
                    
                    # Check for date in column 1 (index 1)
                    if len(row) > 1 and row[1]:
                        date_match = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', str(row[1]).strip())
                        if date_match:
                            current_date = str(row[1]).strip()
                    
                    # Check for time in column 1 (index 1)
                    if len(row) > 1 and row[1]:
                        time_match = re.match(r'(\d+):(\d+)(am|pm)', str(row[1]).strip())
                        if time_match:
                            current_time = str(row[1]).strip()
                    
                    # Search for Poole in the row
                    if current_date and current_time:
                        for col_idx, cell in enumerate(row):
                            if cell and 'poole' in str(cell).lower():
                                # Calculate sheet number
                                # Columns: 0,1,2 = Date/Time; 3,4,5 = Sheet 1; 6,7,8 = Sheet 2; etc.
                                # Sheet 1 starts at index 3
                                if col_idx >= 3:
                                    sheet_num = ((col_idx - 3) // 3) + 1
                                    
                                    # Find opponent in same column group
                                    sheet_start_col = 3 + (sheet_num - 1) * 3
                                    opponent = "Unknown"
                                    
                                    # Look in the same sheet's columns in previous or next row
                                    for check_row_idx in [row_idx - 1, row_idx + 1]:
                                        if 0 <= check_row_idx < len(table):
                                            check_row = table[check_row_idx]
                                            if len(check_row) > col_idx:
                                                potential_opponent = str(check_row[col_idx]).strip()
                                                if (potential_opponent and 
                                                    potential_opponent != 'None' and 
                                                    'poole' not in potential_opponent.lower() and
                                                    len(potential_opponent) > 0 and
                                                    not re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', potential_opponent) and
                                                    not re.match(r'\d+:\d+(am|pm)', potential_opponent)):
                                                    opponent = potential_opponent
                                                    break
                                    
                                    # Check for combined cell (like "Poole Birrell..." which means multiple games)
                                    cell_text = str(cell).strip()
                                    if '\n' in cell_text:
                                        # Multiple games in one cell - parse them
                                        lines = cell_text.split('\n')
                                        for line in lines:
                                            teams = line.split()
                                            if 'poole' in line.lower():
                                                poole_idx = -1
                                                for i, team in enumerate(teams):
                                                    if 'poole' in team.lower():
                                                        poole_idx = i
                                                        break
                                                if poole_idx >= 0:
                                                    # Get opponent (adjacent team)
                                                    if poole_idx % 2 == 0 and poole_idx + 1 < len(teams):
                                                        opponent = teams[poole_idx + 1]
                                                    elif poole_idx > 0:
                                                        opponent = teams[poole_idx - 1]
                                    
                                    games.append({
                                        'date': current_date,
                                        'time': current_time,
                                        'sheet': sheet_num,
                                        'opponent': opponent,
                                        'league': league_name
                                    })
    
    return games

def extract_roster():
    """Extract roster from Excel (manually entered based on previous output)"""
    monday_players = [
        "John Poole",
        "Riley Fairbanks",
        "Curtis Fairhurst",
        "Sheldon Cameron"
    ]
    
    tuesday_players = [
        "John Poole",
        "Brendan Nickles",
        "Ryan Duckworth",
        "Doug Annable"
    ]
    
    return monday_players, tuesday_players

# Extract schedules
print("Extracting Monday Night schedule...")
monday_games = parse_schedule_tables(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Monday Night Mens 2025 2026 28 1st Round - 28 teams.pdf",
    "Monday Night"
)

print("Extracting Tuesday Night schedule...")
tuesday_games = parse_schedule_tables(
    r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\Tuesday Night Mens 2025 2026 1st Round 26 teams.pdf",
    "Tuesday Night"
)

# Extract rosters
monday_roster, tuesday_roster = extract_roster()

# Build final data structure
poole_data = {
    "team_name": "Poole",
    "leagues": [],
    "schedule": [],
    "rosters": []
}

if monday_games:
    poole_data["leagues"].append("Monday Night")
if tuesday_games:
    poole_data["leagues"].append("Tuesday Night")

# Combine all games
all_games = monday_games + tuesday_games
poole_data["schedule"] = all_games

# Add rosters
if monday_roster:
    poole_data["rosters"].append({
        "league": "Monday Night",
        "players": monday_roster
    })
if tuesday_roster:
    poole_data["rosters"].append({
        "league": "Tuesday Night",
        "players": tuesday_roster
    })

# Print summary
print("\n" + "=" * 80)
print(f"TEAM: {poole_data['team_name']}")
print("=" * 80)
print(f"\nLeagues: {', '.join(poole_data['leagues'])}")
print(f"Total Games: {len(poole_data['schedule'])}")
print(f"  Monday Night: {len(monday_games)} games")
print(f"  Tuesday Night: {len(tuesday_games)} games")

print("\n" + "=" * 80)
print("COMPLETE SCHEDULE")
print("=" * 80)
for game in sorted(all_games, key=lambda x: (x['date'], x['time'])):
    print(f"{game['league']:15} | {game['date']:>10} | {game['time']:>7} | Sheet {game['sheet']} | vs {game['opponent']}")

print("\n" + "=" * 80)
print("ROSTERS")
print("=" * 80)
for roster in poole_data["rosters"]:
    print(f"\n{roster['league']}:")
    for i, player in enumerate(roster['players'], 1):
        print(f"  {i}. {player}")

# Save to JSON
output_file = 'poole_team_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(poole_data, f, indent=2, ensure_ascii=False)

print(f"\n✓ Data saved to: {output_file}")
print("\nThis JSON file is ready for use in your GitHub web page database.")

# Also print the JSON structure
print("\n" + "=" * 80)
print("JSON STRUCTURE PREVIEW")
print("=" * 80)
print(json.dumps(poole_data, indent=2, ensure_ascii=False))
