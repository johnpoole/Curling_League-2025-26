import pdfplumber
import json
import re

def parse_friday_schedule_correct():
    """Extract Poole games using table structure"""
    games = []
    
    pdf_path = "Friday Night Mixed 2025 2026 1st Round 26 teams.pdf"
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract as table
            tables = page.extract_tables()
            
            if tables:
                for table in tables:
                    current_date = None
                    date_row_teams = None
                    
                    for row_idx, row in enumerate(table):
                        if not row:
                            continue
                        
                        # Find date in row
                        date_found = None
                        for cell in row[:3]:  # Date is in first few columns
                            if cell:
                                date_match = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', str(cell).strip())
                                if date_match:
                                    date_found = f"{date_match.group(1)} {date_match.group(2)}"
                                    break
                        
                        if date_found:
                            current_date = date_found
                            # This row has first team for each sheet
                            date_row_teams = row
                            continue
                        
                        # Check if this is a time row
                        time_found = None
                        for cell in row[:3]:  # Time is in first few columns
                            if cell:
                                time_match = re.match(r'(\d+):(\d+)\s*(am|pm)', str(cell).strip(), re.IGNORECASE)
                                if time_match:
                                    time_found = f"{time_match.group(1)}:{time_match.group(2)}{time_match.group(3).lower()}"
                                    break
                        
                        if time_found and current_date and date_row_teams:
                            time_str = time_found
                            time_row_teams = row
                            
                            # Process each sheet (every 3 columns starting at column 3)
                            # Columns 0-2: Date/Time
                            # Columns 3-5: Sheet 1
                            # Columns 6-8: Sheet 2, etc.
                            for sheet_num in range(1, 9):  # 8 sheets max
                                col_start = (sheet_num - 1) * 3 + 3
                                col_end = col_start + 3
                                
                                if col_start >= len(date_row_teams):
                                    break
                                
                                # Get team names from both rows for this sheet
                                date_teams = [str(cell).strip() if cell else '' for cell in date_row_teams[col_start:col_end]]
                                time_teams = [str(cell).strip() if cell else '' for cell in time_row_teams[col_start:col_end]]
                                
                                # Find non-empty team names
                                team1 = next((t for t in date_teams if t and t != 'None'), None)
                                team2 = next((t for t in time_teams if t and t != 'None'), None)
                                
                                if not team1 or not team2:
                                    continue
                                
                                # Check if Poole is playing
                                if 'poole' in team1.lower():
                                    opponent = team2
                                    game = {
                                        "date": current_date,
                                        "time": time_str,
                                        "sheet": sheet_num,
                                        "opponent": opponent,
                                        "league": "Friday Night Mixed"
                                    }
                                    games.append(game)
                                    print(f"Found: {current_date} {time_str} Sheet {sheet_num} - Poole vs {opponent}")
                                
                                elif 'poole' in team2.lower():
                                    opponent = team1
                                    game = {
                                        "date": current_date,
                                        "time": time_str,
                                        "sheet": sheet_num,
                                        "opponent": opponent,
                                        "league": "Friday Night Mixed"
                                    }
                                    games.append(game)
                                    print(f"Found: {current_date} {time_str} Sheet {sheet_num} - {opponent} vs Poole")
                            
                            # Reset for next date
                            date_row_teams = None
    
    return games

if __name__ == "__main__":
    print("Parsing Friday schedule using table structure...\n")
    games = parse_friday_schedule_correct()
    
    print(f"\n\nTotal games found: {len(games)}")
    
    # Save to file
    with open('friday_games_corrected.json', 'w') as f:
        json.dump(games, f, indent=2)
    
    print("Saved to friday_games_corrected.json")
