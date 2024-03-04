import numpy as np
import pathlib

file_name = "available_gestures.npy"
file = pathlib.Path(f'./data/{file_name}')

def reset_gesture_list():
    # Actions that we try to detect
    gestures = np.array(['toggle_light', 'increase_brightness', 'decrease_brightness'])
    save_gestures_to_file(gestures)
    print("Gesture list reset !!")

def load_gestures():
    gestures = np.load(file)
    return gestures

def save_gestures_to_file(actions):
    # Save the actions to a numpy array to the gestures file
    np.save(file, actions)

def show_available_gestures():
    gestures = load_gestures()
    print(gestures)

def add_gesture():
    gestures = load_gestures()
    print("Old list of gestures: "+str(gestures))
    print("Try to follow the following naming convention for best result -")
    print("1. Keep the name lowercase")
    print("2. Try to have one word name or words separated by underscore only")
    new_gesture = input("Enter the new gesture name:")
    gestures = np.append(gestures, new_gesture)
    print("New list of gestures: "+str(gestures))
    should_save = input("Save (Y/N): ").upper()
    if should_save == 'Y':
        save_gestures_to_file(gestures)
        print("Saved to "+file_name)
        print("Remember to retrain the model and save the model !!")
    else:
        print("Did not save to the file "+file_name)

def main():
    import os
    choice = 0
    while(choice!=9):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("List of actions related to the gesture list: ")
        print("1. View all gestures")
        print("2. Add new gesture")
        print("3. Reset gesture list")
        print("9. Exit program")
        choice = int(input())
        if choice == 1:
            show_available_gestures()
        elif choice == 2:
            add_gesture()
        elif choice == 3:
            reset_gesture_list()
        elif choice == 9:
            break
        if input("Continue (Y/N): ").upper() == 'Y':
            continue
        else:
            break

if __name__ == '__main__':
    main()