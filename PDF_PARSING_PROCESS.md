# PDF Schedule Parsing Process

## CRITICAL: PDF Table Structure

ALL PDFs (Monday, Tuesday, Friday) use the SAME structure:

```
Date      Sheet 1  Sheet 2  Sheet 3  Sheet 4  ...
Oct 17    TeamA    TeamC    TeamE    TeamG
6:15pm    TeamB    TeamD    TeamF    TeamH
```

**Each sheet column has TWO teams that play EACH OTHER:**
- Sheet 1: TeamA vs TeamB
- Sheet 2: TeamC vs TeamD
- etc.

**Date and Time are in SEPARATE rows!**
- First row after date: contains first team for each sheet
- Second row (with time): contains second team for each sheet (opponent)

## Parsing Algorithm

### Step 1: Identify Date Rows
- Look for lines starting with month abbreviation + day number
- Example: "Oct 17", "Nov 24"

### Step 2: Identify Time Rows
- Next line after date row starts with time pattern: "6:15pm", "8:00pm"

### Step 3: Parse Teams by Column
For each date+time pair:
1. Extract all teams from date row (skip first column which is date)
2. Extract all teams from time row (skip first column which is time)
3. Pair them up positionally:
   - teams_date[0] vs teams_time[0] = Sheet 1
   - teams_date[1] vs teams_time[1] = Sheet 2
   - teams_date[2] vs teams_time[2] = Sheet 3
   - etc.

### Step 4: Find Poole Games
Check BOTH rows (date and time) for "Poole":
- If Poole is in date row at position i: opponent is teams_time[i]
- If Poole is in time row at position i: opponent is teams_date[i]
- Sheet number = i + 1

## Example Walkthrough

PDF lines:
```
Oct 24 Vogt Goehring Hall Bell Rooney Clark Bernbaum Upturns
6:15pm Newton Annable Burnt Rocks Ford Poole House Hunters Rollins Worth
```

Date row teams: [Vogt, Goehring, Hall, Bell, Rooney, Clark, Bernbaum, Upturns]
Time row teams: [Newton, Annable, Burnt Rocks, Ford, Poole, House Hunters, Rollins, Worth]

Matchups:
- Sheet 1: Vogt vs Newton
- Sheet 2: Goehring vs Annable
- Sheet 3: Hall vs Burnt Rocks
- Sheet 4: Bell vs Ford
- Sheet 5: Rooney vs Poole ← WAIT, this is wrong!

Actually, teams can be multi-word! "Burnt Rocks" and "House Hunters" are single teams.

## REAL Problem: Multi-word Team Names

Some teams have spaces:
- "Burnt Rocks"
- "House Hunters"
- "Plan B"
- "Plaid Lads"

Can't just split by spaces! Need to use known team list or better parsing.
