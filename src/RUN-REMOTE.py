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


if __name__ == "__main__":
    sshProcess = create_cmd()
    run_cmd(sshProcess, "cd Project/OLED")
    # Update Project from git
    run_cmd(sshProcess, "git pull https://github.com/ZephCreations/Remote_OLED_control master")

    # Activate venv
    run_cmd(sshProcess, "source venv/bin/activate")
    # Start file
    run_cmd(sshProcess, "python -m src.main")
    # Deactivate venv
    run_cmd(sshProcess, "deactivate")

    run_cmd(sshProcess, "logout")
    print_output(sshProcess)


# output, error = process.communicate()

# print("Output", output, error)


