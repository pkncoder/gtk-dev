import subprocess


def runCommand(command, capture_output=True, text=True, stdin=False):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=text,
            check=True,
            stdin=stdin,
        )
        output = result.stdout

    except subprocess.CalledProcessError as e:
        output = f"Error executing command: {e}"

    except FileNotFoundError:
        output = "Error: Command not found."

    return output
