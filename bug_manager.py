from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from bug import Bug
from storage_manager import StorageManager


class BugManager:
   

    valid_severities = ["Low", "Medium", "High", "Critical"]
    valid_priorities = ["Low", "Medium", "High", "Critical"]
    valid_statuses = ["Open", "In Progress", "Resolved", "Closed"]

    def __init__(self, storage: StorageManager) -> None:
        self.storage = storage
        self.bugs: List[Bug] = self.storage.load_data()

    def generate_bug_id(self) -> str:
        
        if not self.bugs:
            return "BUG-001"

        numbers = []
        for bug in self.bugs:
            try:
                numbers.append(int(bug.bug_id.split("-")[1]))
            except (IndexError, ValueError):
                continue

        next_number = max(numbers, default=0) + 1
        return f"BUG-{next_number:03d}"

    def add_bug(
        self,
        title: str,
        description: str,
        module: str,
        severity: str,
        priority: str,
        reporter: str,
        assignee: str,
    ) -> Bug:
       
        bug = Bug(
            bug_id=self.generate_bug_id(),
            title=title.strip(),
            description=description.strip(),
            module=module.strip(),
            severity=severity,
            priority=priority,
            status="Open",
            reporter=reporter.strip(),
            assignee=assignee.strip() if assignee.strip() else "Unassigned",
            created_date=datetime.now().strftime("%Y-%m-%d"),
        )
        self.bugs.append(bug)
        self.storage.save_data(self.bugs)
        return bug

    def get_all_bugs(self) -> List[Bug]:
        
        return self.bugs

    def find_bug_by_id(self, bug_id: str) -> Optional[Bug]:
        
        for bug in self.bugs:
            if bug.bug_id.lower() == bug_id.lower().strip():
                return bug
        return None

    def update_bug(self, bug_id: str, updates: Dict[str, str]) -> bool:
        
        bug = self.find_bug_by_id(bug_id)
        if bug is None:
            return False

        for field, value in updates.items():
            if hasattr(bug, field) and value.strip():
                setattr(bug, field, value.strip())

        self.storage.save_data(self.bugs)
        return True

    def delete_bug(self, bug_id: str) -> bool:
        
        bug = self.find_bug_by_id(bug_id)
        if bug is None:
            return False

        self.bugs.remove(bug)
        self.storage.save_data(self.bugs)
        return True

    def search_bug(self, keyword: str) -> List[Bug]:

        
        keyword = keyword.lower().strip()
        if not keyword:
            return []

        return [
            bug
            for bug in self.bugs
            if keyword in bug.bug_id.lower() or keyword in bug.title.lower()
        ]

    def filter_bugs(self, field_name: str, value: str) -> List[Bug]:
        
        value = value.lower().strip()
        return [
            bug
            for bug in self.bugs
            if getattr(bug, field_name, "").lower() == value
        ]

    def sort_bugs(self, sort_by: str) -> List[Bug]:

        
        priority_order = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

        if sort_by == "created_date":
            return sorted(self.bugs, key=lambda bug: bug.created_date)
        if sort_by == "priority":
            return sorted(
                self.bugs,
                key=lambda bug: priority_order.get(bug.priority, 0),
                reverse=True,
            )
        if sort_by == "severity":
            return sorted(
                self.bugs,
                key=lambda bug: priority_order.get(bug.severity, 0),
                reverse=True,
            )
        return self.bugs

    def get_overdue_bugs(self, days: int = 3) -> List[Bug]:

        
        today = datetime.now()
        overdue_bugs: List[Bug] = []

        for bug in self.bugs:
            if bug.status in ["Resolved", "Closed"]:
                continue
            try:
                created = datetime.strptime(bug.created_date, "%Y-%m-%d")
            except ValueError:
                continue
            age = (today - created).days
            if age > days:
                overdue_bugs.append(bug)

        return overdue_bugs

    def get_top_priority_bugs(self, limit: int = 3) -> List[Bug]:

        
        open_bugs = [bug for bug in self.bugs if bug.status in ["Open", "In Progress"]]
        ranked = sorted(open_bugs, key=lambda bug: bug.priority_score(), reverse=True)
        return ranked[:limit]

    def get_duplicate_warnings(self, title: str) -> List[Bug]:

        
        title_words = set(title.lower().split())
        matches: List[Bug] = []

        for bug in self.bugs:
            bug_words = set(bug.title.lower().split())
            common_words = title_words.intersection(bug_words)
            if len(common_words) >= 2:
                matches.append(bug)

        return matches

    def generate_reports(self) -> Dict[str, object]:
        
        total = len(self.bugs)
        open_count = len([bug for bug in self.bugs if bug.status == "Open"])
        in_progress_count = len([bug for bug in self.bugs if bug.status == "In Progress"])
        resolved_count = len([bug for bug in self.bugs if bug.status == "Resolved"])
        closed_count = len([bug for bug in self.bugs if bug.status == "Closed"])
        critical_count = len([bug for bug in self.bugs if bug.severity == "Critical"])

        bugs_by_module: Dict[str, int] = {}
        developer_workload: Dict[str, int] = {}

        for bug in self.bugs:
            bugs_by_module[bug.module] = bugs_by_module.get(bug.module, 0) + 1
            developer_workload[bug.assignee] = developer_workload.get(bug.assignee, 0) + 1

        return {
            "total": total,
            "open": open_count,
            "in_progress": in_progress_count,
            "resolved": resolved_count,
            "closed": closed_count,
            "critical": critical_count,
            "bugs_by_module": bugs_by_module,
            "developer_workload": developer_workload,
        }
