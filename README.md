# Curling League 2025-26 - Team Poole Schedule

## Website Files (Root)
- `index.html` - Main website
- `poole_team_data.json` - Schedule and roster data
- `fila-vintage-settanta-track-top-fila-red-lm161rn1-31__45601.jpg` - Team logo

## Folders
- **source_data/** - Excel rosters and PDF schedules
- **scripts/** - Python scripts for data extraction and processing
- **temp_data/** - Intermediate/temporary JSON files
- **.venv/** - Python virtual environment

## Running the Website
```powershell
python -m http.server 8000
```
Then open http://localhost:8000

## Data Structure
The website reads from `poole_team_data.json` which contains:
- `schedule[]` - All games (Monday Night, Tuesday Night, Friday Night Mixed)
- `all_team_rosters{}` - Team rosters organized by team name and league
- `standings{}` - Win/loss records by league
