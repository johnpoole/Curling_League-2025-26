import json
import re

# Load the data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Clean up all_team_rosters
cleaned_rosters = {}
removed_teams = []

for team_name, leagues in data['all_team_rosters'].items():
    # Skip if it looks like a phone number
    if re.match(r'^\d{3}[-.]?\d{4}', team_name):
        removed_teams.append(f"{team_name} (phone number)")
        continue
    
    # Skip single letters
    if len(team_name) == 1:
        removed_teams.append(f"{team_name} (single letter)")
        continue
    
    # Skip if all leagues have empty rosters
    has_players = False
    for league, players in leagues.items():
        if players and len(players) > 0:
            # Check if any player is not a phone number
            valid_players = [p for p in players if not re.match(r'^\d{3}[-.]\d{3}[-.]\d{4}', p)]
            if valid_players:
                has_players = True
                break
    
    if not has_players:
        removed_teams.append(f"{team_name} (no players)")
        continue
    
    # Clean up player lists - remove phone numbers
    cleaned_leagues = {}
    for league, players in leagues.items():
        if players:
            cleaned_players = [p for p in players if not re.match(r'^\d{3}[-.]\d{3}[-.]\d{4}', p)]
            if cleaned_players:
                cleaned_leagues[league] = cleaned_players
    
    if cleaned_leagues:
        cleaned_rosters[team_name] = cleaned_leagues

data['all_team_rosters'] = cleaned_rosters

# Save
with open('poole_team_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("="*80)
print("CLEANED TEAM ROSTERS")
print("="*80)
print(f"\nRemoved {len(removed_teams)} invalid entries:")
for team in removed_teams:
    print(f"  ✗ {team}")

print(f"\nKept {len(cleaned_rosters)} valid teams")
print("\n✓ Cleaned data saved to poole_team_data.json")
