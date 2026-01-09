import json

with open('poole_team_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

friday_games = [g for g in d['schedule'] if g['league'] == 'Friday Night Mixed']
opponents = sorted(set(g['opponent'] for g in friday_games))

roster_teams = sorted([k for k, v in d['all_team_rosters'].items() if 'Friday Night Mixed' in v])

print(f"Total Friday games: {len(friday_games)}")
print(f"Unique opponents: {len(opponents)}")
print(f"Teams with rosters: {len(roster_teams)}\n")

print("Schedule opponents:")
for o in opponents:
    has_roster = "OK" if o in roster_teams else "MISSING"
    print(f"  {has_roster} {o}")

print(f"\nRoster teams (first 15):")
for t in roster_teams[:15]:
    print(f"  {t}")

print("\n\nMissing rosters:")
missing = [opp for opp in opponents if opp not in roster_teams]
if missing:
    for opp in missing:
        print(f"  ❌ {opp}")
else:
    print("  None - all opponents have rosters!")
