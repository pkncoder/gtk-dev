import subprocess


# TODO: Use Gio.HANDELS_COMMAND_LINE proporley
def runCommand(
    command, shell=True, capture_output=True, text=True, check=True, input=""
):
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=text,
            check=check,
            input=input,
        )
        output = [result.stdout, result.stderr, result.returncode]

    except subprocess.CalledProcessError as e:
        output = [f"Error executing command: {e}", "", ""]

    except FileNotFoundError:
        output = ["Error: Command not found.", "", ""]

    return output
