from scripts.commandline_functions import *
import os

def check_python_version():
    import sys
    from global_variables.fixed import PYTHON_MAJOR_VERSION_REQ, PYTHON_MINOR_VERSION_REQ_MAX, PYTHON_MINOR_VERSION_REQ_MIN
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
    from global_variables.user_specific import VIRTUAL_ENV_NAME
    print(f"Checking if {VIRTUAL_ENV_NAME} virtual environment exists ... ",end='')
    if os.path.isdir(VIRTUAL_ENV_NAME):
        issue_success()
        check_status_of_venv()
    else:
        issue_failure()
        print_in_red(f"Virtual environment {VIRTUAL_ENV_NAME} doesn't exist! Run project_setup.py again!")        

def check_all_packages():
    import importlib
    from global_variables.user_specific import VIRTUAL_ENV_NAME
    from global_variables.fixed import REQUIRED_PACKAGES
    print(f"Checking the availability of all packages in the system")
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
    from global_variables.user_specific import CAMERA_NUMBER
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
                print_in_red("Camera feed is not accessible. Try changing the camera number in global_variables/user-specific.py")
    elif choice == 'm':
        from scripts.camera_feed_testing import main
        ret_code = main()
        if ret_code == 0:
            issue_success()
        else:
            issue_failure()
    else:
        issue_warning()
        print_in_yellow(f"\'{choice}\' is an invalid choice! Camera feed testing skipped!")
    feed.release()

def main():
    check_python_version()
    check_virtual_env()
    check_all_packages()
    is_camera_feed_working()

if __name__ == '__main__':
    main()