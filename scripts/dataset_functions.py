from commandline_functions import *
from global_variables.user_specific import *
from gestures_functions import load_gestures

def dataset_folder_exists():
    if not folder_exist(os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME)):
        return False
    else:
        return True
    
def create_folder_structure_for_new_data(actions, num_of_videos, data_path):
    import os
    import numpy as np
    print(f"Creating folder structure for the new data ... ", end='')
    dir_maxes = []
    for action in actions: 
        try:
            dirmax = np.max(np.array(os.listdir(os.path.join(data_path, action))).astype(int)) + 1
        except:
            dirmax = 0
        dir_maxes.append(dirmax)
        for sequence in range(num_of_videos):
            try: 
                os.makedirs(os.path.join(data_path, action, str(dirmax+sequence)))
            except:
                issue_failure()
    issue_success()
    return dir_maxes

def actual_collection_of_videos(actions, num_of_videos, data_path, previous_maxs):
    
    import numpy as np
    import cv2
    from mediapipe_functions import get_mediapipe_variables, draw_styled_landmarks, mediapipe_detection, extract_keypoints

    feed = cv2.VideoCapture(CAMERA_NUMBER)
    mp_holistic, _ = get_mediapipe_variables()
    # Videos are going to be 30 frames in length
    video_length = EACH_VIDEO_FRAME_LENGTH #frames

    # OpenCV Variables
    green = (0, 255, 0)
    blue = (0, 0, 255)

    announcement_position = (120, 200)
    announcement_font_size = 1
    announcement_font = cv2.FONT_HERSHEY_SIMPLEX
    announcement_color = green
    annoucement_line_width = 4
    annoucement_line_type = cv2.LINE_AA

    text_position = (15, 12)
    text_font_size = 0.5
    text_font = cv2.FONT_HERSHEY_SIMPLEX
    text_color = blue
    text_line_width = 1
    text_line_type = cv2.LINE_AA

    print(f"Collection of data in progress ... ")

    # Set mediapipe model 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        
        # Loop through actions
        for action_index in range(len(actions)):
            action = actions[action_index]
            data_folder_start = previous_maxs[action_index]
            # Loop through videos
            for sequence in range(data_folder_start, data_folder_start + num_of_videos):
                # Loop through video length aka sequence length
                for frame_num in range(video_length):

                    # Read feed
                    ret, frame = feed.read()

                    if ret != True:
                        issue_failure()
                        print(in_red(f"Something is wrong!. Camera feed not accessible"))
                        break

                    # Make detections
                    image, results = mediapipe_detection(frame, holistic)

                    # Draw landmarks
                    draw_styled_landmarks(image, results)

                    # Flip the feed frame in x-axis
                    image = cv2.flip(image, 1)
                    
                    # NEW Apply wait logic
                    if frame_num == 0: 
                        cv2.putText(
                            image, 
                            'STARTING COLLECTION', 
                            announcement_position, 
                            announcement_font, 
                            announcement_font_size, 
                            announcement_color, 
                            annoucement_line_width, 
                            annoucement_line_type
                        )
                        cv2.putText(
                            image, 
                            f'Collecting frames for "{action}" video Number {sequence}', 
                            text_position, 
                            text_font, 
                            text_font_size, 
                            text_color, 
                            text_line_width, 
                            text_line_type
                        )
                        # Show to screen
                        cv2.imshow(WINDOW_NAME, image)
                        cv2.waitKey(FRAME_COLLECTION_WAIT_TIME)
                    else: 
                        cv2.putText(
                            image, 
                            f'Collecting frames for "{action}" video number {sequence}', 
                            text_position, 
                            text_font, 
                            text_font_size, 
                            text_color, 
                            text_line_width, 
                            text_line_type
                        )
                        # Show to screen
                        cv2.imshow(WINDOW_NAME, image)
                    
                    # NEW Export keypoints
                    keypoints = extract_keypoints(results, should_print=False)
                    full_path_to_frame = os.path.join(data_path, action, str(sequence), str(frame_num))
                    np.save(full_path_to_frame, keypoints)

                    # Break gracefully
                    if cv2.waitKey(10) & 0xFF == ord(CAMERA_FEED_EXIT_CHAR):
                        break

        feed.release()
        cv2.destroyAllWindows()
    
    issue_success()

def collect_data():
    actions = load_gestures()
    # Path for exported data, numpy arrays
    data_path = os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME)
    # Thirty videos worth of data
    num_of_videos = NUMBER_OF_VIDEOS_FOR_EACH_GESTURE
    previous_maxs = create_folder_structure_for_new_data(actions, num_of_videos, data_path)
    actual_collection_of_videos(actions, num_of_videos, data_path, previous_maxs)
    
def print_current_dataset_details():
    if dataset_folder_exists():
        dataset_is_empty, _ = is_dir_empty(os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME))
        if dataset_is_empty:
            print(in_yellow(f"Dataset folder found but no data found"))
            return
        for gesture in load_gestures():
            if not folder_exist(os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME, gesture), show_output=False):
                print(in_yellow(f"Dataset folder not found for {gesture}."))
            else:
                file_exist(os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME, gesture, '0/0.npy'), show_output=False)
                _, videos = is_dir_empty(os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME, gesture))
                print(in_green(in_italics(f"{gesture} [{len(videos)} videos]")))

def clean_dataset():
    if not dataset_folder_exists():
        print(in_red(f"There is no training dataset folder in the project!"))
        return
    training_data_folder = os.path.join("..", DATA_FOLDER, TRAINING_DATA_FOLDER_NAME)
    is_empty, dir_content = is_dir_empty(training_data_folder)
    if is_empty:
        print(in_yellow(f"Training dataset at {training_data_folder} is already empty!"))
        return
    else:
        print(in_yellow(f"The dataset had folders for {len(dir_content)} gestures. Going to delete them ... "), end='')
    try:
        import shutil
        shutil.rmtree(training_data_folder)
        issue_success()
        print(in_green("Training dataset folder removed !"))
    except:
        issue_failure()
        print(in_red(f"There was a problem deleting the dataset folder. Try deleting {training_data_folder} manually in the project"))

def main():
    from global_variables.user_specific import NUMBER_OF_VIDEOS_FOR_EACH_GESTURE
    import os
    choice = 0
    while(choice!=9):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("List of actions related to the stored dataset: ")
        print("1. Print the dataset details.")
        print("2. Add more data to the dataset for training. ")
        print(in_yellow(f"This will let you add {NUMBER_OF_VIDEOS_FOR_EACH_GESTURE} videos to every gesture into the dataset"))
        print("3. Clean the dataset and remove the folder")
        print("9. Exit program")
        choice = int(input(in_bold("Choice: ")))
        if choice == 1:
            print_current_dataset_details()
        elif choice == 2:
            collect_data()
        elif choice == 3:
            clean_dataset()
        elif choice == 9:
            break
        if input("Continue (Y/N): ").upper() == 'Y':
            continue
        else:
            break

if __name__ == '__main__':
    main()