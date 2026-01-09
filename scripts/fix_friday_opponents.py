import json

# Load data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Create mapping from schedule names to roster names
# Based on analysis of rosters and schedule
name_mapping = {
    "Annable": "The Takeouts",  # Doug Annable is in The Takeouts
    "Clark": "Team 4",          # Jon Clark is in Team 4
    "Worth": "Team Worth",      # Already have Team Worth
    # Rest should match directly: Ford, Loczy, Rollins, Flock
}

print("Fixing Friday opponent names...")
count = 0
for game in data['schedule']:
    if game['league'] == 'Friday Night Mixed':
        old_opponent = game['opponent']
        if old_opponent in name_mapping:
            game['opponent'] = name_mapping[old_opponent]
            print(f"  {old_opponent} -> {game['opponent']}")
            count += 1

# Save updated data
with open('poole_team_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Updated {count} opponent names")
