from __future__ import annotations

from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from bug import Bug
from bug_manager import BugManager


class CLIApp:
    

    def __init__(self, manager: BugManager) -> None:
        self.manager = manager
        self.console = Console()

    def run(self) -> None:
        
        while True:
            self.show_menu()
            choice = Prompt.ask("Enter your choice").strip()

            if choice == "1":
                self.handle_add()
            elif choice == "2":
                self.handle_view_all()
            elif choice == "3":
                self.handle_search()
            elif choice == "4":
                self.handle_filter()
            elif choice == "5":
                self.handle_update()
            elif choice == "6":
                self.handle_delete()
            elif choice == "7":
                self.handle_sort()
            elif choice == "8":
                self.handle_reports()
            elif choice == "9":
                self.console.print("\n[bold green]Data saved. Goodbye![/bold green]")
                break
            else:
                self.console.print("[bold red]Invalid choice. Please try again.[/bold red]")

    def show_menu(self) -> None:
        """Display the main menu."""
        menu_text = (
            "1. Add Bug\n"
            "2. View All Bugs\n"
            "3. Search Bug\n"
            "4. Filter Bugs\n"
            "5. Update Bug\n"
            "6. Delete Bug\n"
            "7. Sort Bugs\n"
            "8. Reports\n"
            "9. Save and Exit"
        )
        self.console.print(Panel(menu_text, title="Smart Bug Tracker CLI", expand=False))

    def display_bugs(self, bugs: List[Bug], title: str = "Bug List") -> None:
        
        if not bugs:
            self.console.print("[bold yellow]No bugs found.[/bold yellow]")
            return

        table = Table(title=title, show_lines=True)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Module")
        table.add_column("Severity")
        table.add_column("Priority")
        table.add_column("Status")
        table.add_column("Reporter")
        table.add_column("Assignee")
        table.add_column("Created")

        for bug in bugs:
            table.add_row(
                bug.bug_id,
                bug.title,
                bug.module,
                bug.severity,
                bug.priority,
                bug.status,
                bug.reporter,
                bug.assignee,
                bug.created_date,
            )

        self.console.print(table)

    def handle_add(self) -> None:
        
        self.console.print("\n[bold cyan]Add New Bug[/bold cyan]")

        title = self.ask_non_empty("Title")
        duplicates = self.manager.get_duplicate_warnings(title)
        if duplicates:
            self.console.print("[bold yellow]Possible duplicate bugs found:[/bold yellow]")
            self.display_bugs(duplicates, "Possible Duplicates")

        description = self.ask_non_empty("Description")
        module = self.ask_non_empty("Module")
        severity = self.ask_choice("Severity", self.manager.valid_severities)
        priority = self.ask_choice("Priority", self.manager.valid_priorities)
        reporter = self.ask_non_empty("Reporter")
        assignee = Prompt.ask("Assignee", default="Unassigned").strip()

        bug = self.manager.add_bug(
            title=title,
            description=description,
            module=module,
            severity=severity,
            priority=priority,
            reporter=reporter,
            assignee=assignee,
        )
        self.console.print(f"[bold green]Bug added successfully: {bug.bug_id}[/bold green]")

    def handle_view_all(self) -> None:
        
        self.display_bugs(self.manager.get_all_bugs(), "All Bugs")

    def handle_search(self) -> None:
        
        keyword = Prompt.ask("Enter bug title or ID to search").strip()
        results = self.manager.search_bug(keyword)
        self.display_bugs(results, "Search Results")

    def handle_filter(self) -> None:
        
        self.console.print("\n1. Filter by Status")
        self.console.print("2. Filter by Severity")
        choice = Prompt.ask("Choose filter option").strip()

        if choice == "1":
            value = self.ask_choice("Status", self.manager.valid_statuses)
            results = self.manager.filter_bugs("status", value)
            self.display_bugs(results, f"Filtered by Status: {value}")
        elif choice == "2":
            value = self.ask_choice("Severity", self.manager.valid_severities)
            results = self.manager.filter_bugs("severity", value)
            self.display_bugs(results, f"Filtered by Severity: {value}")
        else:
            self.console.print("[bold red]Invalid filter option.[/bold red]")

    def handle_update(self) -> None:
        
        bug_id = Prompt.ask("Enter bug ID to update").strip()
        bug = self.manager.find_bug_by_id(bug_id)

        if bug is None:
            self.console.print("[bold red]Bug not found.[/bold red]")
            return

        self.console.print("Press Enter to keep old value.")
        title = Prompt.ask("Title", default=bug.title).strip()
        description = Prompt.ask("Description", default=bug.description).strip()
        module = Prompt.ask("Module", default=bug.module).strip()
        severity = self.ask_choice("Severity", self.manager.valid_severities, allow_blank=True, current=bug.severity)
        priority = self.ask_choice("Priority", self.manager.valid_priorities, allow_blank=True, current=bug.priority)
        status = self.ask_choice("Status", self.manager.valid_statuses, allow_blank=True, current=bug.status)
        reporter = Prompt.ask("Reporter", default=bug.reporter).strip()
        assignee = Prompt.ask("Assignee", default=bug.assignee).strip()

        updated = self.manager.update_bug(
            bug_id,
            {
                "title": title,
                "description": description,
                "module": module,
                "severity": severity,
                "priority": priority,
                "status": status,
                "reporter": reporter,
                "assignee": assignee,
            },
        )

        if updated:
            self.console.print("[bold green]Bug updated successfully.[/bold green]")
        else:
            self.console.print("[bold red]Update failed.[/bold red]")

    def handle_delete(self) -> None:
        
        bug_id = Prompt.ask("Enter bug ID to delete").strip()
        bug = self.manager.find_bug_by_id(bug_id)

        if bug is None:
            self.console.print("[bold red]Bug not found.[/bold red]")
            return

        confirm = Prompt.ask(f"Are you sure you want to delete {bug_id}? (y/n)", default="n").strip().lower()
        if confirm != "y":
            self.console.print("[bold yellow]Delete cancelled.[/bold yellow]")
            return

        deleted = self.manager.delete_bug(bug_id)
        if deleted:
            self.console.print("[bold green]Bug deleted successfully.[/bold green]")
        else:
            self.console.print("[bold red]Delete failed.[/bold red]")

    def handle_sort(self) -> None:
        
        self.console.print("\n1. Sort by Priority")
        self.console.print("2. Sort by Severity")
        self.console.print("3. Sort by Date")
        choice = Prompt.ask("Choose sort option").strip()

        if choice == "1":
            bugs = self.manager.sort_bugs("priority")
            self.display_bugs(bugs, "Sorted by Priority")
        elif choice == "2":
            bugs = self.manager.sort_bugs("severity")
            self.display_bugs(bugs, "Sorted by Severity")
        elif choice == "3":
            bugs = self.manager.sort_bugs("created_date")
            self.display_bugs(bugs, "Sorted by Date")
        else:
            self.console.print("[bold red]Invalid sort option.[/bold red]")

    def handle_reports(self) -> None:
        
        while True:
            report_menu = (
                "1. Total Bug Summary\n"
                "2. Open vs Resolved\n"
                "3. Critical Bugs\n"
                "4. Bugs by Module\n"
                "5. Developer Workload\n"
                "6. Top Priority Bugs\n"
                "7. Overdue Bugs\n"
                "8. Back to Main Menu"
            )
            self.console.print(Panel(report_menu, title="Reports", expand=False))
            choice = Prompt.ask("Choose report option").strip()
            reports = self.manager.generate_reports()

            if choice == "1":
                self.console.print(f"Total Bugs: [bold]{reports['total']}[/bold]")
            elif choice == "2":
                self.console.print(f"Open: [bold]{reports['open']}[/bold]")
                self.console.print(f"In Progress: [bold]{reports['in_progress']}[/bold]")
                self.console.print(f"Resolved: [bold]{reports['resolved']}[/bold]")
                self.console.print(f"Closed: [bold]{reports['closed']}[/bold]")
            elif choice == "3":
                self.console.print(f"Critical Bugs: [bold red]{reports['critical']}[/bold red]")
            elif choice == "4":
                self.display_simple_report_table("Module", "Count", reports["bugs_by_module"])
            elif choice == "5":
                self.display_simple_report_table("Developer", "Assigned Bugs", reports["developer_workload"])
            elif choice == "6":
                self.display_bugs(self.manager.get_top_priority_bugs(), "Top Priority Bugs")
            elif choice == "7":
                self.display_bugs(self.manager.get_overdue_bugs(), "Overdue Bugs")
            elif choice == "8":
                break
            else:
                self.console.print("[bold red]Invalid report option.[/bold red]")

    def display_simple_report_table(self, first_column: str, second_column: str, data: dict) -> None:
        
        if not data:
            self.console.print("[bold yellow]No report data found.[/bold yellow]")
            return

        table = Table(show_lines=True)
        table.add_column(first_column)
        table.add_column(second_column)

        for key, value in data.items():
            table.add_row(str(key), str(value))

        self.console.print(table)

    def ask_non_empty(self, field_name: str) -> str:
        
        while True:
            value = Prompt.ask(field_name).strip()
            if value:
                return value
            self.console.print(f"[bold red]{field_name} cannot be empty.[/bold red]")

    def ask_choice(
        self,
        field_name: str,
        choices: List[str],
        allow_blank: bool = False,
        current: str = "",
    ) -> str:
        
        choice_text = ", ".join(choices)
        while True:
            prompt_text = f"{field_name} ({choice_text})"
            if allow_blank and current:
                value = Prompt.ask(prompt_text, default=current).strip()
            else:
                value = Prompt.ask(prompt_text).strip()

            if allow_blank and not value:
                return current
            if value in choices:
                return value
            self.console.print(f"[bold red]Invalid {field_name}. Choose from: {choice_text}[/bold red]")
