import openpyxl
import json
import re

# Load the Excel file
wb = openpyxl.load_workbook('2025 2026 Curling Roster All Leagues (1).xlsx')
sheet = wb['Mixed']

print("Extracting Friday Night Mixed rosters...\n")

# Read all data
data = []
for row in sheet.iter_rows(values_only=True):
    data.append(row)

rosters = {}

# Process column by column (teams are in columns, 2 columns per team: name + email)
# Look for team indicators: numbers or "Team X - Name"
for col_idx in range(0, len(data[0]), 2):  # Step by 2 (name, email pairs)
    team_name = None
    players = []
    
    for row_idx, row in enumerate(data):
        if col_idx >= len(row):
            continue
            
        cell = row[col_idx]
        
        # Skip empty cells
        if not cell:
            continue
        
        cell_str = str(cell).strip()
        
        # Check if this is a team name/number
        # Pattern 1: Just a number like "5", "6", etc.
        if cell_str.isdigit() and 1 <= int(cell_str) <= 30:
            # If we had a previous team, save it
            if team_name and players:
                rosters[team_name] = players
                print(f"{team_name}: {players}")
            # Start new team
            team_name = cell_str
            players = []
            continue
        
        # Pattern 2: "Team X" or "Team X - Name"
        if cell_str.startswith('Team '):
            # If we had a previous team, save it
            if team_name and players:
                rosters[team_name] = players
                print(f"{team_name}: {players}")
            
            # Extract team name
            if ' - ' in cell_str:
                parts = cell_str.split(' - ', 1)
                team_name = parts[1].strip()
            else:
                # Just "Team 1", "Team 2", etc. - we'll use first player's last name
                team_name = cell_str
            players = []
            continue
        
        # Pattern 3: Number with name like "12 - House Hunters"
        match = re.match(r'^(\d+)\s*-\s*(.+)$', cell_str)
        if match:
            # If we had a previous team, save it
            if team_name and players:
                rosters[team_name] = players
                print(f"{team_name}: {players}")
            
            team_name = match.group(2).strip()
            players = []
            continue
        
        # Otherwise, if we have a team started, this might be a player
        if team_name:
            # Filter out emails and non-names
            if ('@' not in cell_str and 
                not cell_str.startswith('403-') and
                not cell_str.startswith('Team Roster') and
                not cell_str.startswith('Friday Mixed') and
                len(cell_str) > 2 and
                ' ' in cell_str):  # Players should have first and last name
                players.append(cell_str)

# Don't forget the last team
if team_name and players:
    rosters[team_name] = players
    print(f"{team_name}: {players}")

# Now fix team names that are just numbers - use first player's last name
final_rosters = {}
for team_name, players in rosters.items():
    if team_name.isdigit() and players:
        # Use last name of first player
        last_name = players[0].split()[-1]
        final_rosters[last_name] = players
    else:
        final_rosters[team_name] = players

print(f"\n\nTotal teams extracted: {len(final_rosters)}")
print("\nTeam names:")
for name in sorted(final_rosters.keys()):
    print(f"  {name}")

# Load existing data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Replace Friday rosters
data['all_team_rosters']['Friday Night Mixed'] = final_rosters

# Save updated data
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Updated Friday Night Mixed rosters")
