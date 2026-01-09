import json
import re

# Monday Night standings (as of Dec 15, 2025)
monday_standings = {
    "Moss": {"wins": 9, "losses": 1, "ties": 0},
    "Birrell": {"wins": 8, "losses": 1, "ties": 1},
    "Erickson": {"wins": 8, "losses": 1, "ties": 1},
    "Ferguson": {"wins": 7, "losses": 2, "ties": 1},
    "Plaid Lads": {"wins": 6, "losses": 4, "ties": 0},
    "Snethun": {"wins": 6, "losses": 4, "ties": 0},
    "Christie": {"wins": 5, "losses": 5, "ties": 0},
    "Poole": {"wins": 3, "losses": 6, "ties": 1},
    "Robinson": {"wins": 3, "losses": 6, "ties": 1},
    "Pinder": {"wins": 2, "losses": 7, "ties": 0},
    "Wright": {"wins": 3, "losses": 7, "ties": 0},
    "Marshall": {"wins": 2, "losses": 7, "ties": 1},
    "Bailey": {"wins": 2, "losses": 8, "ties": 0},
    "Cameron": {"wins": 2, "losses": 8, "ties": 0},
    "Bonyai": {"wins": 9, "losses": 1, "ties": 0},
    "Carson": {"wins": 8, "losses": 2, "ties": 0},
    "Linder": {"wins": 7, "losses": 3, "ties": 0},
    "Kennedy": {"wins": 6, "losses": 3, "ties": 1},
    "Fairbanks": {"wins": 6, "losses": 4, "ties": 0},
    "Phelps": {"wins": 6, "losses": 4, "ties": 0},
    "Kelly": {"wins": 5, "losses": 4, "ties": 1},
    "Kerbals": {"wins": 4, "losses": 6, "ties": 0},
    "Martin": {"wins": 3, "losses": 6, "ties": 1},
    "Williams": {"wins": 3, "losses": 6, "ties": 1},
    "Bowman": {"wins": 2, "losses": 6, "ties": 2},
    "Fairhurst": {"wins": 2, "losses": 6, "ties": 2},
    "O'Neil": {"wins": 2, "losses": 6, "ties": 2},
    "Gregg": {"wins": 2, "losses": 8, "ties": 0}
}

# Tuesday Night standings (as of Dec 16, 2025)
tuesday_standings = {
    "Balderston": {"wins": 8, "losses": 1, "ties": 2},
    "Waddell": {"wins": 8, "losses": 1, "ties": 2},
    "Johnson": {"wins": 7, "losses": 4, "ties": 0},
    "Poole": {"wins": 7, "losses": 4, "ties": 0},
    "Linder": {"wins": 6, "losses": 4, "ties": 1},
    "The Pants": {"wins": 6, "losses": 4, "ties": 1},
    "Larsen": {"wins": 5, "losses": 4, "ties": 2},
    "Crushmore": {"wins": 4, "losses": 4, "ties": 3},
    "Rollins": {"wins": 5, "losses": 6, "ties": 0},
    "Boog": {"wins": 3, "losses": 6, "ties": 2},
    "Nickles": {"wins": 3, "losses": 8, "ties": 0},
    "MACH": {"wins": 2, "losses": 8, "ties": 1},
    "Brill": {"wins": 1, "losses": 10, "ties": 0},
    "Kennedy": {"wins": 11, "losses": 0, "ties": 0},
    "Moss": {"wins": 10, "losses": 1, "ties": 0},
    "Henry": {"wins": 8, "losses": 3, "ties": 0},
    "Duckworth": {"wins": 7, "losses": 4, "ties": 0},
    "Kohlenberg": {"wins": 6, "losses": 5, "ties": 0},
    "Smith": {"wins": 5, "losses": 5, "ties": 1},
    "Moody": {"wins": 5, "losses": 6, "ties": 0},
    "Clark": {"wins": 4, "losses": 6, "ties": 1},
    "Annable": {"wins": 4, "losses": 7, "ties": 0},
    "Flock": {"wins": 3, "losses": 7, "ties": 2},
    "Curl Jam": {"wins": 3, "losses": 8, "ties": 0},
    "Only Up": {"wins": 2, "losses": 9, "ties": 0},
    "Cole": {"wins": 1, "losses": 10, "ties": 0}
}

# Load existing data
with open('poole_team_data.json', 'r') as f:
    data = json.load(f)

# Add standings to the data structure
data['standings'] = {
    'Monday Night': monday_standings,
    'Tuesday Night': tuesday_standings
}

# Save back
with open('poole_team_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ Standings data added to poole_team_data.json")
print(f"\nMonday Night: {len(monday_standings)} teams")
print(f"Tuesday Night: {len(tuesday_standings)} teams")
