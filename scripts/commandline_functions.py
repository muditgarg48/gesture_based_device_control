import subprocess
import os

def print_in_bold(message):
    print('\033[1m' + message + '\033[0m')

def print_in_italics(message):
    print('\033[3m' + message + '\033[0m')

def print_in_red(message):
    print('\033[31m' + message + '\033[0m')

def print_in_green(message):
    print('\033[32m' + message + '\033[0m')

def print_in_yellow(message):
    print('\033[33m' + message + '\033[0m')


def issue_success():
    import time
    time.sleep(1)
    print("✅")

def issue_warning():
    import time
    time.sleep(1)
    print("⚠️")

def issue_failure():
    import time
    time.sleep(2)
    print("❌")

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