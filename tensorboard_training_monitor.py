import os
from user_defined_global_variables import LOGGER_FOLDER_NAME

def launch_tensorboard_monitor():
    # os.system('ls' if os.name == 'nt' else 'dir')
    os.system(f'cd {LOGGER_FOLDER_NAME}')
    os.system('cd train')
    os.system('tensorboard --logdir=.')

def main():
    launch_tensorboard_monitor()

if __name__ == '__main__':
    main()