# Smart Bug Tracker CLI

A simple Python CLI midterm project built with OOP, JSON storage, and the `rich` library.

## Features

- Add bug
- View all bugs
- Search bug by ID or title
- Filter bugs by status or severity
- Update bug
- Delete bug
- Sort bugs by priority, severity, or date
- Reports:
  - total bug summary
  - open vs resolved
  - critical bugs
  - bugs by module
  - developer workload
  - top priority bugs
  - overdue bugs
- Duplicate title warning
- JSON save and load

## Project Structure

- `main.py` → starts the program
- `bug.py` → Bug entity class
- `bug_manager.py` → business logic class
- `storage_manager.py` → JSON storage class
- `cli_app.py` → CLI controller class
- `data/bugs.json` → saved bug data
- `requirements.txt` → external library list

## macOS Setup

```bash
mkdir -p ~/Desktop/python_midterm_projects
cd ~/Desktop/python_midterm_projects
cp -R /path/to/smart_bug_tracker_cli .
cd smart_bug_tracker_cli
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Freeze requirements

```bash
pip freeze > requirements.txt
```

# PROGRAMMING_IN_PYTHON_Group07
# PROGRAMMING_IN_PYTHON_Group07
