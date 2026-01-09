import json

# Load data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Get the wrongly structured Friday rosters
friday_rosters_wrong = data['all_team_rosters'].get('Friday Night Mixed', {})

# Remove the wrong structure
if 'Friday Night Mixed' in data['all_team_rosters']:
    del data['all_team_rosters']['Friday Night Mixed']

# Restructure properly: each team should have Friday Night Mixed as a sub-key
for team_name, players in friday_rosters_wrong.items():
    if team_name not in data['all_team_rosters']:
        data['all_team_rosters'][team_name] = {}
    data['all_team_rosters'][team_name]['Friday Night Mixed'] = players

print(f"Restructured {len(friday_rosters_wrong)} Friday teams")

# Save
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Fixed Friday Night Mixed roster structure")
