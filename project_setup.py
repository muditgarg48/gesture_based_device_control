import os
import subprocess

def run_command(command):
    proc = subprocess.Popen(command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result_code = proc.wait()
    return result_code

def run_command_and_show_output(command):
    proc = subprocess.Popen(command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        print(proc.stdout.readline())
    result_code = proc.wait()
    return result_code

def issue_success():
    import time
    time.sleep(0.5)
    print("✅")

def issue_warning():
    import time
    time.sleep(0.5)
    print("⚠️")

def issue_failure():
    import time
    time.sleep(0.5)
    print("❌")

def file_exist(file_name):
    print(f"Checking {file_name} ... ", end='')
    if os.path.isfile(file_name):
        issue_success()
    else:
        issue_failure()

def print_weird_behaviour(result_code):
    print(f"\nWeird result code running the script. Error code {result_code}")

def activate_venv_command():
    from global_variables import virtual_env_name
    if os.name=='nt':
        return f'"{virtual_env_name}/Scripts/activate.bat"'
    else:
        return f'"{virtual_env_name}/Scripts/activate"'

def check_python():
    print("Checking for Python installation ... ", end='')
    result_code = run_command("python --version")
    if result_code == 0:
        issue_success()
    elif result_code == 1:
        issue_failure()
        print("Try reinstalling Python and running this script again")
    else:
        print_weird_behaviour(result_code)

def check_pip():
    print("Checking for Pip installation ... ", end='')
    result_code = run_command("pip --version")
    if result_code == 0:
        issue_success()    
    elif result_code == 1:
        issue_warning()
        install_pip()
    else:
        print_weird_behaviour(result_code)

def install_pip():
    print("Downloading Pip ... ", end='')
    if run_command("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py") == 0:
        issue_success()
    else:
        issue_failure()
    print("Installing Pip ... ", end='')
    if run_command("python get-pip.py") == 0:
        issue_success()
    else:
        issue_failure()

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
    if run_command("pip install virtualenv") == 0:
        issue_success()
    else:
        issue_failure()

def check_virtual_environment():
    from global_variables import virtual_env_name
    print(f"Checking if {virtual_env_name} virtual environment exists ... ",end='')
    if os.path.isdir(virtual_env_name):
        issue_success()
        activate_venv()
        install_dependencies()
    else:
        issue_warning()
        create_virtual_environment()

def create_virtual_environment():
    import os
    from global_variables import virtual_env_name
    print(f"Creating virtual environment named {virtual_env_name} ... ",end='')
    if run_command(f"python -m venv {virtual_env_name}") == 0:
        issue_success()
        check_status_of_venv()
    else:
        issue_failure()

def check_status_of_venv():
    import sys
    print("Is the virtual environment activated ... ", end='')
    if sys.prefix == sys.base_prefix:
        issue_warning()
        print(f"Current virtual environment: {sys.base_prefix}")
        activate_venv()
    else:
        issue_success()
        print(f"Virtual environment active: {sys.prefix}")

def activate_venv():
    import os
    from global_variables import virtual_env_name
    print(f"Activating {virtual_env_name} to install dependencies, using ",end='')
    command = activate_venv_command()
    print(f" {command} ... ", end='')
    if run_command(command) == 0:
        issue_success()
        install_dependencies()
    else:
        issue_failure()
        print(f"Sorry couldn't activate the {virtual_env_name} environment to install dependencies")
        print("⚠️  Enable virtual environment manually and try restarting the script if this fails again on retry !")
        print(f"Command: {command}")
        exit()

def install_dependencies():
    print("Installing dependencies from requirements.txt file, this may take a while. ")
    print("⚠️  Data charges may apply")
    import time
    time.sleep(1)
    if run_command_and_show_output("pip install -r requirements.txt") == 0:
        print("Installation completed ... ", end='')
        issue_success()
    else:
        print("Installation interrupted ... ", end='')
        issue_warning()

def main():
    check_python()
    file_exist("requirements.txt")
    check_pip()
    check_venv_package()
    check_virtual_environment()
    command = activate_venv_command()
    print(f"Setup completed !! Activate the virtual virtual environment using {command} and run the project. ", end='')
    issue_success()
    
if __name__ == '__main__':
    main()