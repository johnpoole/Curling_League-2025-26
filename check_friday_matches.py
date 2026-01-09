import json

# Load current data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Get Friday teams from rosters
friday_rosters = data['all_team_rosters'].get('Friday Night Mixed', {})

print("Current Friday teams in rosters:")
for team in sorted(friday_rosters.keys()):
    print(f"  {team}")

print("\nOpponents in schedule:")
friday_games = [g for g in data['schedule'] if g['league'] == 'Friday Night Mixed']
opponents = sorted(set(g['opponent'] for g in friday_games))
for opp in opponents:
    print(f"  {opp}")

print("\n\nMatching opponents to rosters:")
for opp in opponents:
    matches = [team for team in friday_rosters.keys() if opp.lower() in team.lower()]
    if matches:
        print(f"  {opp} -> {matches}")
    else:
        print(f"  {opp} -> NO MATCH")
