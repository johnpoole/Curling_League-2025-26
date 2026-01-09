import json

# Load existing data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Load Friday games
with open('friday_games.json', 'r') as f:
    friday_games = json.load(f)

# Add Friday Night Mixed to leagues if not already there
if "Friday Night Mixed" not in data['leagues']:
    data['leagues'].append("Friday Night Mixed")

# Add Friday games to schedule
data['schedule'].extend(friday_games)

# Sort schedule by date (rough sort by month)
month_order = {'Oct': 10, 'Nov': 11, 'Dec': 12, 'Jan': 1, 'Feb': 2, 'Mar': 3}

def sort_key(game):
    month, day = game['date'].split()
    month_num = month_order.get(month, 0)
    # Adjust for year (Jan-Mar are 2026, Oct-Dec are 2025)
    if month_num <= 3:
        month_num += 12
    return (month_num, int(day), game['time'])

data['schedule'].sort(key=sort_key)

# Save updated data
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Added {len(friday_games)} Friday Night Mixed games to schedule")
print(f"  Total games: {len(data['schedule'])}")
print(f"  Leagues: {data['leagues']}")
