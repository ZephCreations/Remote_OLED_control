import platform
from pathlib import Path

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


#######################################################################
#                          REMOTE commands
#######################################################################
import subprocess
user = "zoot"
host = "192.168.1.33"
password = "password"

def create_cmd():
    return subprocess.Popen(["ssh", '-tt', f'{user}@{host}'],
                            universal_newlines=True,
                            bufsize=0,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def print_output(process: subprocess.Popen):
    for line in process.stdout:
        print(line, end="")


def run_cmd(process: subprocess.Popen, cmd):
    process.stdin.write(f"{cmd}\r")
