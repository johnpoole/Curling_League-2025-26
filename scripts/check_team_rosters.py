import json

d = json.load(open('poole_team_data.json'))

teams_to_check = ['Team 1', 'Team 2', 'Vogt']

for t in teams_to_check:
    if t in d['all_team_rosters'] and 'Friday Night Mixed' in d['all_team_rosters'][t]:
        players = d['all_team_rosters'][t]['Friday Night Mixed']
        print(f"{t}: {players}")
