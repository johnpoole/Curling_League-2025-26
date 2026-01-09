import json

# Load data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Mappings from PDF names to roster team names
name_mapping = {
    "Annable": "The Takeouts",
    "Bernbaum": "Team Bernbaum",
    "Clark": "Team 4",
    "Upturns": "The Upturns",
    "Worth": "Team Worth",
    # Newton: NOT FOUND IN ROSTERS - need to check Excel
}

print("Updating Friday opponent names...")
count = 0
for game in data['schedule']:
    if game['league'] == 'Friday Night Mixed':
        old_opponent = game['opponent']
        if old_opponent in name_mapping:
            game['opponent'] = name_mapping[old_opponent]
            print(f"  {old_opponent} → {game['opponent']}")
            count += 1

# Save
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Updated {count} opponent names")
print("\n⚠️  WARNING: 'Newton' not found in rosters - may need manual check")
