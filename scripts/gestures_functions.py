import numpy as np
import pathlib
from scripts.global_variables.user_specific import DATA_FOLDER
from scripts.commandline_functions import *

def reset_gesture_list(file_path):
    # Actions that we try to detect
    gestures = np.array(['toggle_light', 'increase_brightness', 'decrease_brightness'])
    save_gestures_to_file(gestures, file_path)
    print("Gesture list reset !!")

def load_gestures(file_path):
    gestures = np.load(file_path)
    return gestures

def get_num_of_gestures(file_path):
    gestures = load_gestures(file_path)
    return len(gestures)

def save_gestures_to_file(actions, file_path):
    # Save the actions to a numpy array to the gestures file
    print(f"Saving {actions} to {file_path}")
    np.save(file_path, actions)

def show_available_gestures(file_path):
    gestures = load_gestures(file_path)
    print(gestures)

def delete_gesture(file_path, file_name):
    gestures = load_gestures(file_path)
    print("Old list of gestures: "+str(gestures))
    del_gesture_index = int(input("Enter the gesture index to delete:"))
    print(f"Want to delete {gestures[del_gesture_index]} ?")
    gestures = np.delete(gestures, del_gesture_index)
    should_save = input("Save (Y/N): ").upper()
    if should_save == 'Y':
        save_gestures_to_file(gestures, file_path)
        print("Saved to "+file_name)
        print("Remember to retrain the model and save the model !!")
        print("New list of gestures: "+str(gestures))
    else:
        print("Did not save to the file "+file_name)

def add_gesture(file_path, file_name):
    gestures = load_gestures(file_path)
    print("Old list of gestures: "+str(gestures))
    print("Try to follow the following naming convention for best result -")
    print("1. Keep the name lowercase")
    print("2. Try to have one word name or words separated by underscore only")
    new_gesture = input("Enter the new gesture name:")
    gestures = np.append(gestures, new_gesture)
    print("New list of gestures: "+str(gestures))
    should_save = input("Save (Y/N): ").upper()
    if should_save == 'Y':
        save_gestures_to_file(gestures, file_path)
        print("Saved to "+file_name)
        print("Remember to retrain the model and save the model !!")
    else:
        print("Did not save to the file "+file_name)

def main():
    file_name = "available_gestures.npy"
    file_path = pathlib.Path(f'../{DATA_FOLDER}/{file_name}')
    import os
    choice = 0
    while(choice!=9):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("List of actions related to the gesture list: ")
        print("1. View all gestures")
        print("2. Add new gesture")
        print("3. Delete existing gesture")
        print("4. Reset gesture list")
        print("9. Exit program")
        choice = int(input(in_bold("Choice: ")))
        if choice == 1:
            show_available_gestures(file_path)
        elif choice == 2:
            add_gesture(file_path, file_name)
        elif choice == 3:
            delete_gesture(file_path, file_name)
        elif choice == 4:
            reset_gesture_list(file_path)
        elif choice == 9:
            break
        if input("Continue (Y/N): ").upper() == 'Y':
            continue
        else:
            break

if __name__ == '__main__':
    main()