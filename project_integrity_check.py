from scripts.commandline_functions import *
import os

def check_python_version():
    import sys
    from scripts.global_variables.fixed import PYTHON_MAJOR_VERSION_REQ, PYTHON_MINOR_VERSION_REQ_MAX, PYTHON_MINOR_VERSION_REQ_MIN
    major_v = sys.version_info[0]
    minor_v = sys.version_info[1]
    micro_v = sys.version_info[2]
    print(f"Python "+in_bold(f"{major_v}.{minor_v}.{micro_v}")+" detected ... ",end='')
    if (major_v < PYTHON_MAJOR_VERSION_REQ) and (minor_v < PYTHON_MINOR_VERSION_REQ_MIN or minor_v > PYTHON_MINOR_VERSION_REQ_MAX):
        issue_failure()
        print(in_red(f"REQUIREMENT: Python version >={PYTHON_MAJOR_VERSION_REQ}.{PYTHON_MINOR_VERSION_REQ_MIN} <={PYTHON_MAJOR_VERSION_REQ}.{PYTHON_MINOR_VERSION_REQ_MAX}"))
    else:
        issue_success()

def check_status_of_venv():
    import sys
    print("Is the virtual environment activated ... ", end='')
    if sys.prefix == sys.base_prefix:
        # print(sys.prefix)
        # print(sys.base_prefix)
        issue_warning()
        print(in_yellow("Activate project's local virtual environment !"))
    else:
        issue_success()
    print(in_italics(f"Current virtual environment: {in_bold(sys.prefix)}"))

def check_virtual_env():
    from scripts.global_variables.user_specific import VIRTUAL_ENV_NAME
    print(f"Checking if {in_bold(VIRTUAL_ENV_NAME)} virtual environment exists ... ",end='')
    if os.path.isdir(VIRTUAL_ENV_NAME):
        issue_success()
        check_status_of_venv()
    else:
        issue_failure()
        print(in_red(f"Virtual environment {in_bold(VIRTUAL_ENV_NAME)} doesn't exist! Run project_setup.py again!"))

def check_all_packages():
    import importlib
    from scripts.global_variables.user_specific import VIRTUAL_ENV_NAME
    from scripts.global_variables.fixed import REQUIRED_PACKAGES
    print("Checking the availability of all packages in the system")
    for package in REQUIRED_PACKAGES:
        package_id = package["id"]
        package_name = package["name"]
        print(f"{package_name} [{in_italics(package_id)}] ... ",end='')
        if importlib.util.find_spec(package_id) is not None:
            issue_success()
        else:
            issue_failure()

def is_camera_feed_working():
    import cv2
    from scripts.global_variables.user_specific import CAMERA_NUMBER
    feed = cv2.VideoCapture(CAMERA_NUMBER)
    choice = input("Test camera feed automatically or manually (A/M): ").lower()
    print("Checking if camera feed is accessible ... ", end='')
    if choice == 'a':    
        while feed.isOpened():
            return_value, frame = feed.read()
            if frame is not None and return_value == True:
                issue_success()
                break
            else:
                issue_failure()
                print(in_red("Camera feed is not accessible. Try changing the camera number in "+in_bold("global_variables/user-specific.py")))
    elif choice == 'm':
        from scripts.camera_feed_testing import main
        ret_code = main()
        if ret_code == 0:
            issue_success()
        else:
            issue_failure()
    else:
        issue_warning()
        print(in_yellow(f"\'{in_bold(choice)}\' is an invalid choice! Camera feed testing skipped!"))
    feed.release()

def print_check():
    print(underline_this(in_bold("Check"))+": ", end='')

def main():
    print_check()
    check_python_version()
    print_check()
    check_virtual_env()
    print_check()
    check_all_packages()
    print_check()
    is_camera_feed_working()

if __name__ == '__main__':
    main()