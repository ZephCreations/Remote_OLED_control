from pathlib import Path

def get_project_root() -> Path:
    path = Path(__file__).parent.parent
    return path
