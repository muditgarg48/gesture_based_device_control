from commandline_functions import *
import os

def check_python_version():
    import sys
    from fixed_global_variables import PYTHON_MAJOR_VERSION_REQ, PYTHON_MINOR_VERSION_REQ_MAX, PYTHON_MINOR_VERSION_REQ_MIN
    print(f"Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} detected ... ",end='')
    major_version = sys.version_info[0]
    minor_version = sys.version_info[1]
    if (major_version < PYTHON_MAJOR_VERSION_REQ) and (minor_version < PYTHON_MINOR_VERSION_REQ_MIN or minor_version > PYTHON_MINOR_VERSION_REQ_MAX):
        issue_failure()
        print_in_red("REQUIREMENT: Python version >=3.9 <=3.11")
    else:
        issue_success()

def check_status_of_venv():
    import sys
    print("Is the virtual environment activated ... ", end='')
    if sys.prefix == sys.base_prefix:
        # print(sys.prefix)
        # print(sys.base_prefix)
        issue_warning()
        print_in_yellow("Activate project's local virtual environment !")
    else:
        issue_success()
    print_in_italics(f"Current virtual environment: {sys.prefix}")

def check_virtual_env():
    from user_defined_global_variables import VIRTUAL_ENV_NAME
    print(f"Checking if {VIRTUAL_ENV_NAME} virtual environment exists ... ",end='')
    if os.path.isdir(VIRTUAL_ENV_NAME):
        issue_success()
        check_status_of_venv()
    else:
        issue_failure()
        print_in_red(f"Virtual environment {VIRTUAL_ENV_NAME} doesn't exist! Run project_setup.py again!")        

def check_all_packages():
    import importlib
    from user_defined_global_variables import VIRTUAL_ENV_NAME
    from fixed_global_variables import REQUIRED_PACKAGES
    print(f"Checking the availability of all packages from {VIRTUAL_ENV_NAME}")
    print("=====================================================================")
    for package in REQUIRED_PACKAGES:
        package_id = package["id"]
        package_name = package["name"]
        print(f"{package_name} [{package_id}] ... ",end='')
        if importlib.util.find_spec(package_id) is not None:
            issue_success()
        else:
            issue_failure()
    print("=====================================================================")

def is_camera_feed_working():
    import cv2
    from user_defined_global_variables import CAMERA_NUMBER
    feed = cv2.VideoCapture(CAMERA_NUMBER)
    print("Checking if camera feed is accessible ... ", end='')
    while feed.isOpened():
        return_value, frame = feed.read()
        if frame is not None:
            issue_success()
            break
        else:
            issue_failure()
            print_in_red("Camera feed is not accesible. Try changing the camera number in global_variables.py")
    feed.release()

def main():
    check_python_version()
    check_virtual_env()
    check_all_packages()
    is_camera_feed_working()

if __name__ == '__main__':
    main()