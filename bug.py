from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class Bug:
    """a single bug record."""

    bug_id: str
    title: str
    description: str
    module: str
    severity: str
    priority: str
    status: str
    reporter: str
    assignee: str
    created_date: str

    def to_dict(self) -> Dict[str, Any]:
        
        return {
            "bug_id": self.bug_id,
            "title": self.title,
            "description": self.description,
            "module": self.module,
            "severity": self.severity,
            "priority": self.priority,
            "status": self.status,
            "reporter": self.reporter,
            "assignee": self.assignee,
            "created_date": self.created_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Bug":
        
        return cls(
            bug_id=data.get("bug_id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            module=data.get("module", ""),
            severity=data.get("severity", "Medium"),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Open"),
            reporter=data.get("reporter", ""),
            assignee=data.get("assignee", "Unassigned"),
            created_date=data.get("created_date", datetime.now().strftime("%Y-%m-%d")),
        )

    def priority_score(self) -> int:
        
        severity_scores = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        priority_scores = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        return severity_scores.get(self.severity, 0) + priority_scores.get(self.priority, 0)
