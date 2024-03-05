import os
import sys
from scripts.commandline_functions import *

# ====================
# Common functions
# ====================

def print_weird_behaviour(result_code):
    print_in_yellow(f"\nWeird result code running the script. Error code {result_code}")

def is_python_3():
    result_code = run_command(["python3 --version"])
    if result_code == 0:
        return True
    else:
        return False

# ============================
# Purpose specific functions
# ============================

def activate_venv_command():
    from scripts.user_defined_global_variables import VIRTUAL_ENV_NAME
    if os.name=='nt':
        return f'"{VIRTUAL_ENV_NAME}/Scripts/activate.bat"'
    else:
        return f'"{VIRTUAL_ENV_NAME}/Scripts/activate"'

def warning_for_installing_dependencies():
    print_in_yellow("This may take a while. Thank you for your patience!")
    print_in_yellow("⚠️  Data charges may apply  ⚠️")
    print_in_bold("================================================================")
    print_in_bold("\t\tPip installation outputs")
    print_in_bold("================================================================")

def check_python():
    from scripts.fixed_global_variables import PYTHON_MAJOR_VERSION_REQ, PYTHON_MINOR_VERSION_REQ_MIN, PYTHON_MINOR_VERSION_REQ_MAX
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
    result_code = run_command(["pip --version"])
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
    if is_python_3() == True:
        result_code = run_command(["python3 get-pip.py"])
    else:
        result_code = run_command(["python get-pip.py"])
    if result_code == 0:
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
    result_code = run_command(["pip install virtualenv"])
    if result_code == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red("Failed to install virtualenv package with pip. Try again or do it manually!")
        exit()

def check_virtual_environment():
    from scripts.user_defined_global_variables import VIRTUAL_ENV_NAME
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
    from scripts.user_defined_global_variables import VIRTUAL_ENV_NAME
    print(f"Creating virtual environment named {VIRTUAL_ENV_NAME} ... ",end='')
    if is_python_3() == True:
        command = f"python3 -m venv {VIRTUAL_ENV_NAME}"
    else:
        command = f"python -m venv {VIRTUAL_ENV_NAME}"
    result_code = run_command_and_show_output([command])
    if result_code == 0:
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
    from scripts.user_defined_global_variables import VIRTUAL_ENV_NAME
    command1 = activate_venv_command()
    command2 = "pip install -r requirements.txt"
    if is_python_3() == True:
        command3 = f'python3 -m ipykernel install --user --name {VIRTUAL_ENV_NAME} --display "Python (my-project)"'
    else:
        command3 = f'python -m ipykernel install --user --name {VIRTUAL_ENV_NAME} --display "Python (my-project)"'
    print_in_italics(f"Activating {VIRTUAL_ENV_NAME} to install dependencies, using {command1} and also checking and installing dependencies ... ")
    warning_for_installing_dependencies()
    commands = [command1, command2, command3]
    result_code = run_command_and_show_output(commands)
    if result_code == 0:
        issue_success()
    else:
        issue_failure()
        print_in_red(f"Sorry either couldn't activate the {VIRTUAL_ENV_NAME} environment to install dependencies")
        print_in_italics("⚠️  Enable virtual environment manually and try restarting the script")
        print_in_bold(f"Command: {command1}")
        print_in_red(f"Or failed while installing dependencies if the Pip installation had started!")
        exit()

def install_dependencies():
    print("Installing/Updating dependencies from requirements.txt file, this may take a while. ")
    warning_for_installing_dependencies()
    command = "pip install -r requirements.txt"
    result_code = run_command_and_show_output([command])
    if result_code == 0:
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
    print_in_bold(f"Activate the virtual virtual environment using {command} to run the project !")
    
if __name__ == '__main__':
    main()