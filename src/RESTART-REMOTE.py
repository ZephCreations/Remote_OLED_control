from utils import create_cmd, run_cmd, print_output


if __name__ == "__main__":
    sshProcess = create_cmd()

    # Reload daemon (for any script changes) and restart service
    run_cmd(sshProcess, "sudo systemctl daemon-reload")

    run_cmd(sshProcess, "sudo systemctl restart oled.service")
    run_cmd(sshProcess, "sudo systemctl status oled.service")

    run_cmd(sshProcess, "exit")
    print_output(sshProcess)


# output, error = process.communicate()

# print("Output", output, error)


