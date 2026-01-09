import json

# Load data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Get Friday roster teams
friday_rosters = {k: v['Friday Night Mixed'] for k, v in data['all_team_rosters'].items() if 'Friday Night Mixed' in v}

print("Searching for Newton in all Friday rosters...\n")

for team_name, players in friday_rosters.items():
    for player in players:
        if 'newton' in player.lower():
            print(f"Found Newton in '{team_name}': {player}")

print("\n\nSearching for Upturns team...\n")
for team_name in friday_rosters.keys():
    if 'upturns' in team_name.lower():
        print(f"Found team: {team_name}")
        print(f"  Players: {friday_rosters[team_name]}")
