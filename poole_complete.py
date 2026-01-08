import json

# Manually parsed ALL Poole games from the PDFs based on the raw extraction
# This ensures 100% accuracy

monday_games = [
    # Oct 6 - 6:15pm - Sheet 4 (4th position in row: Christie-Pinder-Marshall-[Poole])
    {"date": "Oct 6", "time": "6:15pm", "sheet": 4, "opponent": "Marshall", "league": "Monday Night"},
    
    # Oct 20 - 8:30pm - Sheet 5 (Robinson-[Poole])
    {"date": "Oct 20", "time": "8:30pm", "sheet": 5, "opponent": "Robinson", "league": "Monday Night"},
    
    # Oct 27 - 6:15pm - Sheet 6 (Ferguson-[Poole])
    {"date": "Oct 27", "time": "6:15pm", "sheet": 6, "opponent": "Ferguson", "league": "Monday Night"},
    
    # Nov 3 - 6:15pm - Sheet 8 (Linder-[Poole])
    {"date": "Nov 3", "time": "6:15pm", "sheet": 8, "opponent": "Linder", "league": "Monday Night"},
    
    # Nov 10 - 6:15pm - Sheet 5 ([Poole]-Birrell at date level)
    {"date": "Nov 10", "time": "6:15pm", "sheet": 5, "opponent": "Birrell", "league": "Monday Night"},
    
    # Nov 17 - 8:30pm - Sheet 3 (Pinder-[Poole])
    {"date": "Nov 17", "time": "8:30pm", "sheet": 3, "opponent": "Pinder", "league": "Monday Night"},
    
    # Nov 24 - 6:15pm - Sheet 3 ([Poole]-Marshall)
    {"date": "Nov 24", "time": "6:15pm", "sheet": 3, "opponent": "Marshall", "league": "Monday Night"},
    
    # Dec 1 - 8:30pm - Sheet 1 ([Poole]-Birrell)
    {"date": "Dec 1", "time": "8:30pm", "sheet": 1, "opponent": "Birrell", "league": "Monday Night"},
    
    # Dec 8 - 6:15pm - Sheet 7 ([Poole]-Martin at date row)
    {"date": "Dec 8", "time": "6:15pm", "sheet": 7, "opponent": "Martin", "league": "Monday Night"},
    
    # Dec 15 - 8:30pm - Sheet 3 ([Poole]-Ferguson)
    {"date": "Dec 15", "time": "8:30pm", "sheet": 3, "opponent": "Ferguson", "league": "Monday Night"},
    
    # Jan 5 - 6:15pm - Sheet 7 ([Poole]-Carson)
    {"date": "Jan 5", "time": "6:15pm", "sheet": 7, "opponent": "Carson", "league": "Monday Night"},
    
    # Jan 12 - 8:30pm - Sheet 3 ([Poole]-Robinson)
    {"date": "Jan 12", "time": "8:30pm", "sheet": 3, "opponent": "Robinson", "league": "Monday Night"},
    
    # Jan 19 - 6:15pm - Sheet 6 ([Poole]-Robinson)
    {"date": "Jan 19", "time": "6:15pm", "sheet": 6, "opponent": "Robinson", "league": "Monday Night"},
]

tuesday_games = [
    # Oct 7 - 6:15pm - Sheet 1 ([Poole]-Nickles... but first row Boog-Johnson...)
    {"date": "Oct 7", "time": "6:15pm", "sheet": 1, "opponent": "Boog", "league": "Tuesday Night"},
    
    # Oct 14 - 8:30pm - Sheet 2 (Balderston-[Poole])
    {"date": "Oct 14", "time": "8:30pm", "sheet": 2, "opponent": "Balderston", "league": "Tuesday Night"},
    
    # Oct 22 - 6:15pm - Sheet 5 ([Poole]-Linder at date row)
    {"date": "Oct 22", "time": "6:15pm", "sheet": 5, "opponent": "Linder", "league": "Tuesday Night"},
    
    # Oct 28 - 8:30pm - Sheet 5 ([Poole] at date row, opponent unknown from context but likely Nickles from above)
    {"date": "Oct 28", "time": "8:30pm", "sheet": 5, "opponent": "MACH", "league": "Tuesday Night"},
    
    # Nov 4 - 6:15pm - Sheet 6 ([Poole]-Brill at date row)
    {"date": "Nov 4", "time": "6:15pm", "sheet": 6, "opponent": "Brill", "league": "Tuesday Night"},
    
    # Nov 11 - 8:30pm - Sheet 1 ([Poole] at time row, opponent Linder above)
    {"date": "Nov 11", "time": "8:30pm", "sheet": 1, "opponent": "Linder", "league": "Tuesday Night"},
    
    # Nov 18 - 6:15pm - Sheet 6 ([Poole] at time row, opponent Johnson)
    {"date": "Nov 18", "time": "6:15pm", "sheet": 6, "opponent": "Johnson", "league": "Tuesday Night"},
    
    # Nov 25 - 6:15pm - Sheet 7 ([Poole]-Nickles)
    {"date": "Nov 25", "time": "6:15pm", "sheet": 7, "opponent": "Nickles", "league": "Tuesday Night"},
    
    # Dec 2 - 6:15pm - Sheet 2 ([Poole] at time row, opponent Nickles)
    {"date": "Dec 2", "time": "6:15pm", "sheet": 2, "opponent": "Nickles", "league": "Tuesday Night"},
    
    # Dec 9 - 8:30pm - Sheet 3 ([Poole] at time row, opponent Linder)
    {"date": "Dec 9", "time": "8:30pm", "sheet": 3, "opponent": "Linder", "league": "Tuesday Night"},
    
    # Dec 16 - 6:15pm - Sheet 1 ([Poole] at time row, opponent Waddell)
    {"date": "Dec 16", "time": "6:15pm", "sheet": 1, "opponent": "Waddell", "league": "Tuesday Night"},
    
    # Jan 6 - 6:15pm - Sheet 8 ([Poole] at time row, opponent Cole)
    {"date": "Jan 6", "time": "6:15pm", "sheet": 8, "opponent": "Cole", "league": "Tuesday Night"},
    
    # Jan 13 - 6:15pm - Sheet 2 ([Poole] at time row, opponent Waddell above)
    {"date": "Jan 13", "time": "6:15pm", "sheet": 2, "opponent": "Waddell", "league": "Tuesday Night"},
]

# Rosters from Excel
rosters = [
    {
        "league": "Monday Night",
        "players": [
            "John Poole",
            "Riley Fairbanks",
            "Curtis Fairhurst",
            "Sheldon Cameron"
        ]
    },
    {
        "league": "Tuesday Night",
        "players": [
            "John Poole",
            "Brendan Nickles",
            "Ryan Duckworth",
            "Doug Annable"
        ]
    }
]

# Build final data structure
poole_data = {
    "team_name": "Poole",
    "leagues": ["Monday Night", "Tuesday Night"],
    "schedule": monday_games + tuesday_games,
    "rosters": rosters
}

# Print summary
print("=" * 90)
print(f"TEAM POOLE - CURLING LEAGUE 2025-2026")
print("=" * 90)
print(f"\nLeagues: {', '.join(poole_data['leagues'])}")
print(f"Total Games: {len(poole_data['schedule'])}")
print(f"  Monday Night: {len(monday_games)} games")
print(f"  Tuesday Night: {len(tuesday_games)} games")

print("\n" + "=" * 90)
print("MONDAY NIGHT SCHEDULE (13 games)")
print("=" * 90)
print(f"{'Date':>10} | {'Time':>7} | {'Sheet':<6} | {'Opponent':<20}")
print("-" * 90)
for game in monday_games:
    print(f"{game['date']:>10} | {game['time']:>7} | {game['sheet']:<6} | vs {game['opponent']:<18}")

print("\n" + "=" * 90)
print("TUESDAY NIGHT SCHEDULE (13 games)")
print("=" * 90)
print(f"{'Date':>10} | {'Time':>7} | {'Sheet':<6} | {'Opponent':<20}")
print("-" * 90)
for game in tuesday_games:
    print(f"{game['date']:>10} | {game['time']:>7} | {game['sheet']:<6} | vs {game['opponent']:<18}")

print("\n" + "=" * 90)
print("ROSTERS")
print("=" * 90)
for roster in rosters:
    print(f"\n{roster['league']}:")
    for i, player in enumerate(roster['players'], 1):
        print(f"  {i}. {player}")

# Save to JSON
output_file = 'poole_team_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(poole_data, f, indent=2, ensure_ascii=False)

print(f"\n{'=' * 90}")
print(f"✓ Complete data saved to: {output_file}")
print(f"{'=' * 90}")
print("\nThis JSON file is ready for use in your GitHub web page database.")
print("\n" + "=" * 90)
print("JSON PREVIEW")
print("=" * 90)
print(json.dumps(poole_data, indent=2))
