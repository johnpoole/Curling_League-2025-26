import json

d = json.load(open('poole_team_data.json'))
games = [g for g in d['schedule'] if g['league'] == 'Friday Night Mixed']

print("First 5 Friday games in data:")
for g in games[:5]:
    print(f"{g['date']} {g['time']} Sheet {g['sheet']} vs {g['opponent']}")
