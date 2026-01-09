import pdfplumber
import json
import re

def parse_friday_schedule():
    """Extract Poole games from Friday Night Mixed schedule"""
    games = []
    
    pdf_path = "Friday Night Mixed 2025 2026 1st Round 26 teams.pdf"
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                # Skip header lines
                if 'RIDAY' in line or 'Sheet' in line and 'Date' in line:
                    continue
                
                # Check if line has a date AND Poole
                date_match = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', line)
                if date_match and 'poole' in line.lower():
                    current_date = f"{date_match.group(1)} {date_match.group(2)}"
                    
                    # Next line should have the time
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        time_match = re.match(r'(\d+):(\d+)\s*(am|pm)', next_line.strip(), re.IGNORECASE)
                        if time_match:
                            time_str = f"{time_match.group(1)}:{time_match.group(2)}{time_match.group(3).lower()}"
                            
                            print(f"Found Poole on {current_date} at {time_str}")
                            print(f"  Date line: {line}")
                            
                            # Extract teams from the date line (not time line)
                            # Remove the date part first
                            teams_part = line[len(date_match.group(0)):].strip()
                            team_parts = teams_part.split()
                            
                            # Find Poole
                            poole_idx = -1
                            for k, part in enumerate(team_parts):
                                if 'poole' in part.lower():
                                    poole_idx = k
                                    break
                            
                            if poole_idx >= 0:
                                # Sheet is based on position (2 teams per sheet)
                                sheet = (poole_idx // 2) + 1
                                
                                # Opponent is the other team in this pair
                                opponent = None
                                if poole_idx % 2 == 0:
                                    # Poole is first, opponent is next
                                    if poole_idx + 1 < len(team_parts):
                                        opponent = team_parts[poole_idx + 1]
                                else:
                                    # Poole is second, opponent is previous
                                    opponent = team_parts[poole_idx - 1]
                                
                                if opponent:
                                    game = {
                                        "date": current_date,
                                        "time": time_str,
                                        "sheet": sheet,
                                        "opponent": opponent,
                                        "league": "Friday Night Mixed"
                                    }
                                    games.append(game)
                                    print(f"  Extracted: Sheet {sheet} vs {opponent}")
                
                # Check if line has a time AND Poole (but no date)
                elif 'poole' in line.lower():
                    time_match = re.match(r'(\d+):(\d+)\s*(am|pm)', line.strip(), re.IGNORECASE)
                    if time_match:
                        time_str = f"{time_match.group(1)}:{time_match.group(2)}{time_match.group(3).lower()}"
                        
                        # Need to find the date - look backwards
                        current_date = None
                        for j in range(i-1, max(0, i-5), -1):
                            prev_line = lines[j]
                            date_match2 = re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d+)', prev_line)
                            if date_match2:
                                current_date = f"{date_match2.group(1)} {date_match2.group(2)}"
                                break
                        
                        if current_date:
                            print(f"Found Poole on {current_date} at {time_str}")
                            print(f"  Time line: {line}")
                            
                            # Extract teams from line
                            parts = line.split()
                            # Remove time part
                            team_parts = [p for p in parts if not re.match(r'\d+:\d+', p) and not re.match(r'am|pm', p, re.IGNORECASE)]
                            
                            # Find Poole
                            poole_idx = -1
                            for k, part in enumerate(team_parts):
                                if 'poole' in part.lower():
                                    poole_idx = k
                                    break
                            
                            if poole_idx >= 0:
                                # Sheet is based on position (2 teams per sheet)
                                sheet = (poole_idx // 2) + 1
                                
                                # Opponent is the other team in this pair
                                opponent = None
                                if poole_idx % 2 == 0:
                                    # Poole is first, opponent is next
                                    if poole_idx + 1 < len(team_parts):
                                        opponent = team_parts[poole_idx + 1]
                                else:
                                    # Poole is second, opponent is previous
                                    opponent = team_parts[poole_idx - 1]
                                
                                if opponent:
                                    game = {
                                        "date": current_date,
                                        "time": time_str,
                                        "sheet": sheet,
                                        "opponent": opponent,
                                        "league": "Friday Night Mixed"
                                    }
                                    games.append(game)
                                    print(f"  Extracted: Sheet {sheet} vs {opponent}")
    
    return games

if __name__ == "__main__":
    print("Parsing Friday Night Mixed schedule...\n")
    games = parse_friday_schedule()
    
    print(f"\n\nFound {len(games)} Poole games:")
    for game in games:
        print(f"  {game['date']} at {game['time']} - Sheet {game['sheet']} vs {game['opponent']}")
    
    # Save to separate file for review
    with open('friday_games.json', 'w') as f:
        json.dump(games, f, indent=2)
    
    print(f"\nSaved to friday_games.json")
