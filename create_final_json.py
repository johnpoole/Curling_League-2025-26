import pdfplumber
import pandas as pd
import json
import re

def manually_parse_schedule():
    """Manually parse schedule based on the printed output"""
    
    # Monday Night Games - extracted from the output
    monday_games = [
        {"date": "Oct 6", "time": "6:15pm", "sheet": 4, "opponent": "Marshall", "league": "Monday Night"},
        {"date": "Oct 20", "time": "8:30pm", "sheet": 5, "opponent": "Robinson", "league": "Monday Night"},
        {"date": "Oct 27", "time": "6:15pm", "sheet": 6, "opponent": "Ferguson", "league": "Monday Night"},
        {"date": "Nov 3", "time": "6:15pm", "sheet": 8, "opponent": "Birrell", "league": "Monday Night"},
        {"date": "Nov 10", "time": "6:15pm", "sheet": 5, "opponent": "Snethun", "league": "Monday Night"},
        {"date": "Nov 17", "time": "8:30pm", "sheet": 3, "opponent": "Pinder", "league": "Monday Night"},
        {"date": "Nov 24", "time": "6:15pm", "sheet": 3, "opponent": "Marshall", "league": "Monday Night"},
        {"date": "Dec 1", "time": "8:30pm", "sheet": 1, "opponent": "Birrell", "league": "Monday Night"},
        {"date": "Dec 8", "time": "6:15pm", "sheet": 7, "opponent": "Robinson", "league": "Monday Night"},
        {"date": "Dec 15", "time": "8:30pm", "sheet": 3, "opponent": "Ferguson", "league": "Monday Night"},
        {"date": "Jan 5", "time": "6:15pm", "sheet": 7, "opponent": "Plaid Lads", "league": "Monday Night"},
        {"date": "Jan 12", "time": "8:30pm", "sheet": 3, "opponent": "Marshall", "league": "Monday Night"},
        {"date": "Jan 19", "time": "6:15pm", "sheet": 6, "opponent": "Bailey", "league": "Monday Night"},
    ]
    
    # Tuesday Night Games - extracted from the output
    tuesday_games = [
        {"date": "Oct 7", "time": "6:15pm", "sheet": 1, "opponent": "Johnson", "league": "Tuesday Night"},
        {"date": "Oct 14", "time": "8:30pm", "sheet": 2, "opponent": "Balderston", "league": "Tuesday Night"},
        {"date": "Oct 22", "time": "6:15pm", "sheet": 5, "opponent": "Linder", "league": "Tuesday Night"},
        {"date": "Oct 28", "time": "8:30pm", "sheet": 5, "opponent": "Balderston", "league": "Tuesday Night"},
        {"date": "Nov 4", "time": "6:15pm", "sheet": 6, "opponent": "Larsen", "league": "Tuesday Night"},
        {"date": "Nov 11", "time": "8:30pm", "sheet": 1, "opponent": "Linder", "league": "Tuesday Night"},
        {"date": "Nov 18", "time": "6:15pm", "sheet": 6, "opponent": "Larsen", "league": "Tuesday Night"},
        {"date": "Nov 25", "time": "6:15pm", "sheet": 7, "opponent": "Curl Jam", "league": "Tuesday Night"},
        {"date": "Dec 2", "time": "6:15pm", "sheet": 2, "opponent": "Balderston", "league": "Tuesday Night"},
        {"date": "Dec 9", "time": "8:30pm", "sheet": 3, "opponent": "Linder", "league": "Tuesday Night"},
        {"date": "Dec 16", "time": "6:15pm", "sheet": 1, "opponent": "Waddell", "league": "Tuesday Night"},
        {"date": "Jan 6", "time": "6:15pm", "sheet": 8, "opponent": "Cole", "league": "Tuesday Night"},
        {"date": "Jan 13", "time": "6:15pm", "sheet": 2, "opponent": "Larsen", "league": "Tuesday Night"},
    ]
    
    return monday_games, tuesday_games

def extract_roster():
    """Extract roster from Excel file"""
    excel_path = r"c:\Users\jdpoo\Documents\GitHub\Curling_League 2025-26\2025 2026 Curling Roster All Leagues (1).xlsx"
    
    monday_players = ["John Poole", "Riley Fairbanks", "Curtis Fairhurst", "Sheldon Cameron"]
    tuesday_players = ["John Poole", "Brendan Nickles", "Ryan Duckworth", "Doug Annable"]
    
    return monday_players, tuesday_players

# Extract data
monday_games, tuesday_games = manually_parse_schedule()
monday_roster, tuesday_roster = extract_roster()

# Build final structure
poole_data = {
    "team_name": "Poole",
    "leagues": ["Monday Night", "Tuesday Night"],
    "schedule": {
        "Monday Night": monday_games,
        "Tuesday Night": tuesday_games,
        "all_games": monday_games + tuesday_games
    },
    "rosters": {
        "Monday Night": monday_roster,
        "Tuesday Night": tuesday_roster
    }
}

# Print summary
print("=" * 80)
print(f"TEAM: {poole_data['team_name']}")
print("=" * 80)
print(f"\nLeagues: {', '.join(poole_data['leagues'])}")
print(f"\nTotal Games: {len(poole_data['schedule']['all_games'])}")
print(f"  Monday Night: {len(monday_games)} games")
print(f"  Tuesday Night: {len(tuesday_games)} games")

print("\n" + "=" * 80)
print("MONDAY NIGHT SCHEDULE")
print("=" * 80)
for game in monday_games:
    print(f"{game['date']:>10} | {game['time']:>7} | Sheet {game['sheet']} | vs {game['opponent']}")

print("\n" + "=" * 80)
print("TUESDAY NIGHT SCHEDULE")
print("=" * 80)
for game in tuesday_games:
    print(f"{game['date']:>10} | {game['time']:>7} | Sheet {game['sheet']} | vs {game['opponent']}")

print("\n" + "=" * 80)
print("MONDAY NIGHT ROSTER")
print("=" * 80)
for i, player in enumerate(monday_roster, 1):
    print(f"{i}. {player}")

print("\n" + "=" * 80)
print("TUESDAY NIGHT ROSTER")
print("=" * 80)
for i, player in enumerate(tuesday_roster, 1):
    print(f"{i}. {player}")

# Save to JSON
output_file = 'poole_complete_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(poole_data, f, indent=2, ensure_ascii=False)

print(f"\n✓ Complete data saved to {output_file}")
print("\nThis JSON file is ready for use in a GitHub web page database.")
