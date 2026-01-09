import openpyxl
import json
import re

# Load the Excel file
wb = openpyxl.load_workbook('2025 2026 Curling Roster All Leagues (1).xlsx')
sheet = wb['Mixed']

# Find all team names and rosters
print("Extracting Friday Night Mixed rosters...\n")

# Get all data from sheet
all_rosters = {}
current_team = None
current_roster = []

for row_idx, row in enumerate(sheet.iter_rows(values_only=True), 1):
    # Check if this is a team name row (has text in first column)
    if row[0] and isinstance(row[0], str) and row[0].strip():
        team_name = row[0].strip()
        
        # Skip header rows
        if team_name in ['Team', 'Name', 'TEAM', 'NAME'] or 'League' in team_name:
            continue
        
        # If we have a previous team, save it
        if current_team and current_roster:
            all_rosters[current_team] = current_roster
            print(f"{current_team}: {len(current_roster)} players")
        
        # Start new team
        current_team = team_name
        current_roster = []
        
        # Check if there are players on this row too (after team name)
        for cell in row[1:]:
            if cell and isinstance(cell, str) and cell.strip():
                player = cell.strip()
                if player and len(player) > 2 and not player.startswith('Team'):
                    current_roster.append(player)
    
    # Check for player names in any column
    elif current_team:
        for cell in row:
            if cell and isinstance(cell, str) and cell.strip():
                player = cell.strip()
                # Filter out obvious non-names
                if (player and len(player) > 2 and 
                    not player.startswith('Team') and 
                    not player.startswith('League') and
                    player not in current_roster):
                    current_roster.append(player)

# Don't forget the last team
if current_team and current_roster:
    all_rosters[current_team] = current_roster
    print(f"{current_team}: {len(current_roster)} players")

print(f"\nTotal teams found: {len(all_rosters)}")

# Load existing data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Add Friday rosters to all_team_rosters under "Friday Night Mixed"
if 'Friday Night Mixed' not in data['all_team_rosters']:
    data['all_team_rosters']['Friday Night Mixed'] = {}

for team_name, roster in all_rosters.items():
    data['all_team_rosters']['Friday Night Mixed'][team_name] = roster

# Save updated data
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Added {len(all_rosters)} Friday Night Mixed team rosters")
