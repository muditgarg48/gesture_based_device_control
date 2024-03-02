import os
import subprocess
import sys
from commandline_msg_highlighting import *

# ====================
# Common functions
# ====================

def run_command(commands):
    command = commands[0]
    if len(commands) > 1:
        for c in commands:
            command += ' && ' + c
    proc = subprocess.Popen(command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result_code = proc.wait()
    return result_code

def run_command_and_show_output(commands):
    command = commands[0]
    if len(commands) > 1:
        for c in commands:
            command += ' && ' + c
    proc = subprocess.Popen(command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        print_in_italics(str(proc.stdout.readline()))
    result_code = proc.wait()
    return result_code

def file_exist(file_name):
    print(f"Checking {file_name} ... ", end='')
    if os.path.isfile(file_name):
        issue_success()
    else:
        issue_failure()
        print_in_yellow(f"Cannot find {file_name}. Might result in unexpected behavior of code.")

def print_weird_behaviour(result_code):
    print_in_yellow(f"\nWeird result code running the script. Error code {result_code}")

# ============================
# Purpose specific functions
# ============================

def activate_venv_command():
    from global_variables import VIRTUAL_ENV_NAME
    if os.name=='nt':
        return f'"{VIRTUAL_ENV_NAME}/Scripts/activate.bat"'
    else:
        return f'"{VIRTUAL_ENV_NAME}/Scripts/activate"'

def warning_for_installing_dependencies():
    print_in_yellow("This may take a while. Thank you for your patience!")
    print_in_italics("⚠️  Data charges may apply  ⚠️")
    print_in_bold("================================================================")
    print_in_bold("\t\tPip installation outputs")
    print_in_bold("================================================================")

def check_python():
    from global_variables import PYTHON_MAJOR_VERSION_REQ, PYTHON_MINOR_VERSION_REQ_MIN, PYTHON_MINOR_VERSION_REQ_MAX
    print("Checking for Python installation ... ", end='')
    major_version = sys.version_info[0]
    minor_version = sys.version_info[1]
    if (major_version < PYTHON_MAJOR_VERSION_REQ) and (minor_version < PYTHON_MINOR_VERSION_REQ_MIN or minor_version > PYTHON_MINOR_VERSION_REQ_MAX):
        issue_failure()
        print_in_red("System environment variables did not find Python version >=3.9 <=3.11")
        print_in_italics("Mediapipe requires these python versions to work!")
        exit()
    else:
        issue_success()

def check_pip():
    print("Checking for Pip installation ... ", end='')
    result_code = run_command(["pip3 --version"])
    if result_code == 0:
        issue_success()    
    elif result_code == 1:
        issue_warning()
        install_pip()
    else:
        print_weird_behaviour(result_code)

def install_pip():
    print("Downloading Pip ... ", end='')
    if run_command(["curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"]) == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red("Maybe check your internet connection!")
        print_in_red("Or download and install pip Python package installer manually!")
        exit()
    print("Installing Pip ... ", end='')
    if run_command(["python3 get-pip.py"]) == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red("Downloaded Pip but couldn't install for some reason. Try manually!")
        exit()

def check_venv_package():
    print("Checking for virtual env package installation ... ", end='')
    try:
        import virtualenv
        issue_success()
    except ImportError as e:
        issue_warning()
        install_virtualenv()

def install_virtualenv():
    print("Installing virtualenv ... ", end='')
    if run_command(["pip3 install virtualenv"]) == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red("Failed to install virtualenv package with pip. Try again or do it manually!")
        exit()

def check_virtual_environment():
    from global_variables import VIRTUAL_ENV_NAME
    print(f"Checking if {VIRTUAL_ENV_NAME} virtual environment exists ... ",end='')
    if os.path.isdir(VIRTUAL_ENV_NAME):
        issue_success()
        if check_status_of_venv() == True:
            install_dependencies()
        else:
            activate_venv_and_install_dependencies()
    else:
        issue_warning()
        create_virtual_environment()
        activate_venv_and_install_dependencies()

def create_virtual_environment():
    import os
    from global_variables import VIRTUAL_ENV_NAME
    print(f"Creating virtual environment named {VIRTUAL_ENV_NAME} ... ",end='')
    command = f"python3 -m venv {VIRTUAL_ENV_NAME} "
    if run_command([command]) == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red("Couldn't create a virtual environment. That is not supposed to NOT happen. Try manually using this following command and try again:")
        print_in_bold(command)
        exit()

def check_status_of_venv():
    import sys
    print("Is the virtual environment activated ... ", end='')
    if sys.prefix == sys.base_prefix:
        issue_warning()
        print_in_italics(f"Current virtual environment: {sys.base_prefix}")
        activate_venv_and_install_dependencies()
        return False
    else:
        issue_success()
        print_in_italics(f"Virtual environment active: {sys.prefix}")
        return True

def activate_venv_and_install_dependencies():
    from global_variables import VIRTUAL_ENV_NAME
    command1 = activate_venv_command()
    command2 = "pip3 install -r requirements.txt"
    command3 = f'python3 -m ipykernel install --user --name {VIRTUAL_ENV_NAME} --display "Python (my-project)"'
    print_in_italics(f"Activating {VIRTUAL_ENV_NAME} to install dependencies, using {command1} and also checking and installing dependencies ... ")
    warning_for_installing_dependencies()
    if run_command_and_show_output([command1, command2, command3]) == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red(f"Sorry either couldn't activate the {VIRTUAL_ENV_NAME} environment to install dependencies")
        print_in_italics("⚠️  Enable virtual environment manually and try restarting the script if this fails again on retry !")
        print_in_bold(f"Command: {command1}")
        print_in_red(f"Or failed while installing dependencies if the Pip installation had started!")
        exit()

def install_dependencies():
    print("Installing/Updating dependencies from requirements.txt file, this may take a while. ")
    warning_for_installing_dependencies()
    if run_command_and_show_output(["pip3 install -r requirements.txt"]) == 0:
        print_in_italics("================================================================")
        print("Installation completed ... ", end='')
        issue_success()
    else:
        print_in_italics("================================================================")
        print("Installation interrupted ... ", end='')
        issue_warning()

def main():
    check_python()
    file_exist("requirements.txt")
    check_pip()
    check_venv_package()
    check_virtual_environment()
    command = activate_venv_command()
    print("Project prerequistes installation completed ", end='')
    issue_success()
    if not check_status_of_venv():
        print_in_bold(f"Activate the virtual virtual environment using {command} and run the project !")
    
if __name__ == '__main__':
    main()