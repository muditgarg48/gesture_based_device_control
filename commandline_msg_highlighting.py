def print_in_bold(message):
    print('\033[1m' + message + '\033[0m')

def print_in_italics(message):
    print('\033[3m' + message + '\033[0m')

def print_in_red(message):
    print('\033[91m' + message + '\033[0m')

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