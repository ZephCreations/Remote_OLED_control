from utils import create_cmd, run_cmd, print_output


if __name__ == "__main__":
    sshProcess = create_cmd()
    run_cmd(sshProcess, "cd Project/OLED")
    # Update Project from git
    # link command for reference:
    #   git init
    #   git remote add origin https://github.com/ZephCreations/Remote_OLED_control.git

    run_cmd(sshProcess, "git fetch origin")
    run_cmd(sshProcess, "git reset --hard origin/master")
    run_cmd(sshProcess, "git pull origin master")

    # Activate venv
    run_cmd(sshProcess, "source venv/bin/activate")
    # Start file
    run_cmd(sshProcess, "python src/main.py")
    # Deactivate venv
    run_cmd(sshProcess, "deactivate")

    run_cmd(sshProcess, "exit")
    print_output(sshProcess)


# output, error = process.communicate()

# print("Output", output, error)


