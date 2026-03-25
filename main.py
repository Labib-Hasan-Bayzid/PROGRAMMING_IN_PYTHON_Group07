from storage_manager import StorageManager
from bug_manager import BugManager
from cli_app import CLIApp


def main() -> None:
    """Create the app objects and run the program."""
    storage = StorageManager("data/bugs.json")
    manager = BugManager(storage)
    app = CLIApp(manager)
    app.run()


if __name__ == "__main__":
    main()
