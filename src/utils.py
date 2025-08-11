from pathlib import Path

def get_project_root() -> Path:
    path = Path(__file__).parent.parent
    print(path)
    print(path.as_posix())
    return path
