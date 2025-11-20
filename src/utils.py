import platform
from pathlib import Path
from platform import system, uname

def get_project_root() -> Path:
    path = Path(__file__).parent.parent
    return path

def is_pi():
    """Return True only when running on a Raspberry Pi."""
    if platform.system() != "Linux":
        return False

    # Raspberry Pi uses BCM CPU with specific identifiers
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read().lower()
        return "raspberry pi" in cpuinfo or "bcm" in cpuinfo
    except FileNotFoundError:
        return False
