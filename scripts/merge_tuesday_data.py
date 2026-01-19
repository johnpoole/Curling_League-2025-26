import json
from datetime import datetime

def parse_date(date_str):
    """Parse date string like 'Oct 7' to comparable format"""
    # Add current year for comparison
    try:
        date_obj = datetime.strptime(f"{date_str} 2025", "%b %d %Y")
        return date_obj
    except:
        # If it fails (e.g., dates in 2026), try 2026
        try:
            date_obj = datetime.strptime(f"{date_str} 2026", "%b %d %Y")
            return date_obj
        except:
            return None

def merge_tuesday_games():
    """Merge Tuesday games into main schedule"""
    
    # Load main data
    with open('../poole_team_data.json', 'r') as f:
        main_data = json.load(f)
    
    # Load Tuesday games
    with open('../temp_data/tuesday_games.json', 'r') as f:
        tuesday_games = json.load(f)
    
    # Get existing schedule
    schedule = main_data['schedule']
    
    # Remove existing Tuesday Night games
    print("Removing existing Tuesday Night games...")
    original_count = len(schedule)
    schedule = [game for game in schedule if game['league'] != 'Tuesday Night']
    removed_count = original_count - len(schedule)
    print(f"Removed {removed_count} existing Tuesday games")
    
    # Add new Tuesday games
    print(f"\nAdding {len(tuesday_games)} new Tuesday games...")
    schedule.extend(tuesday_games)
    
    # Sort schedule by date
    def sort_key(game):
        date_obj = parse_date(game['date'])
        if date_obj:
            # If month is Oct-Dec, use 2025; if Jan-Apr, use 2026
            month = date_obj.month
            if month >= 10:  # Oct, Nov, Dec
                year = 2025
            else:  # Jan through Sep
                year = 2026
            return datetime(year, month, date_obj.day)
        return datetime.max  # Put unparseable dates at end
    
    schedule.sort(key=sort_key)
    
    # Update main data
    main_data['schedule'] = schedule
    
    # Save back to file
    with open('../poole_team_data.json', 'w') as f:
        json.dump(main_data, f, indent=2)
    
    print(f"\n✓ Successfully merged Tuesday games")
    print(f"Total games in schedule: {len(schedule)}")
    
    # Count games by league
    league_counts = {}
    for game in schedule:
        league = game['league']
        league_counts[league] = league_counts.get(league, 0) + 1
    
    print("\nGames by league:")
    for league, count in sorted(league_counts.items()):
        print(f"  {league}: {count} games")

if __name__ == "__main__":
    merge_tuesday_games()
