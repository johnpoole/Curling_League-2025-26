import json

# Load corrected games
with open('friday_games_corrected.json', 'r') as f:
    corrected_games = json.load(f)

# Load main data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Remove old Friday games
data['schedule'] = [g for g in data['schedule'] if g['league'] != 'Friday Night Mixed']

# Add corrected Friday games
data['schedule'].extend(corrected_games)

# Sort schedule
month_order = {'Oct': 10, 'Nov': 11, 'Dec': 12, 'Jan': 1, 'Feb': 2, 'Mar': 3}

def sort_key(game):
    month, day = game['date'].split()
    month_num = month_order.get(month, 0)
    if month_num <= 3:
        month_num += 12
    return (month_num, int(day), game['time'])

data['schedule'].sort(key=sort_key)

# Save
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Replaced Friday games with corrected schedule")
print(f"  Total games: {len(data['schedule'])}")
