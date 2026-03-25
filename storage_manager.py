from __future__ import annotations

import json
from pathlib import Path
from typing import List

from bug import Bug


class StorageManager:
    

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> List[Bug]:
        
        if not self.file_path.exists():
            self.save_data([])
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

        if not isinstance(raw_data, list):
            return []

        bugs: List[Bug] = []
        for item in raw_data:
            if isinstance(item, dict):
                bugs.append(Bug.from_dict(item))
        return bugs

    def save_data(self, bugs: List[Bug]) -> None:
        
        data = [bug.to_dict() for bug in bugs]
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
