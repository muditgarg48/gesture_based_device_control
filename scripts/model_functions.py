from commandline_functions import *
from global_variables.user_specific import DATA_FOLDER, MODEL_SAVE_LOCATION, EACH_VIDEO_FRAME_LENGTH
import os
models_loc = os.path.join('..', DATA_FOLDER, MODEL_SAVE_LOCATION)
colors = [(245,117,16), (117,245,16), (16,117,245)]
model_extension = '.h5'

def build_neural_network(num_of_frames, num_of_actions, num_of_features=126):
    from keras.models import Sequential
    from keras.layers import LSTM, Dense
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(num_of_frames, num_of_features)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_of_actions, activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

    return model

def ask_for_model_name():
    print(in_yellow("You do not need to mention the extension of the model!!"))
    model_name = input(f"Enter the name of the existing model to be tested from {in_bold(models_loc)}:")
    if model_name[-3:] == model_extension:
        print(in_yellow(f"Its useless to type {in_bold(model_extension)} as well!!"))
        model_name = model_name[:-3]
    return model_name

def train_model_on_data():
    import os
    import numpy as np
    from sklearn.model_selection import train_test_split
    from keras.utils import to_categorical
    from gestures_functions import load_gestures
    from global_variables.user_specific import DATA_FOLDER, TRAINING_DATA_FOLDER_NAME, EACH_VIDEO_FRAME_LENGTH

    print(in_yellow("Make sure to start the "+in_bold("tensorboard_training_monitor.py")+" script in a separate terminal to have an interactive monitoring of your training progress"))

    print("Importing gestures from storage ...", end='')
    try:
        actions = load_gestures()
        issue_success()
    except:
        issue_failure()
        print(in_red("Something went wrong!"))
        exit()
    label_map = {label:num for num, label in enumerate(actions)}
    videos, labels = [], []
    data_path = os.path.join('..', DATA_FOLDER, TRAINING_DATA_FOLDER_NAME)
    video_len = EACH_VIDEO_FRAME_LENGTH
    print("Importing data for every gesture from dataset ...", end='')
    try:
        for action in actions:
            for video in np.array(os.listdir(os.path.join(data_path, action))).astype(int):
                video_window = []
                for frame_num in range(video_len):
                    res = np.load(os.path.join(data_path, action, str(video), f"{frame_num}.npy"))
                    video_window.append(res)
                videos.append(video_window)
                labels.append(label_map[action])
        issue_success()
    except:
        issue_failure()
        print(in_red("Something went wrong in accumulating all numpy arrays in one for every gesture!"))
        exit()
    X = np.array(videos)
    y = to_categorical(labels).astype(int)
    print(in_bold("Dataset shape: "))
    from global_variables.user_specific import NUMBER_OF_VIDEOS_FOR_EACH_GESTURE, EACH_VIDEO_FRAME_LENGTH
    correct_videos_shape = f"({NUMBER_OF_VIDEOS_FOR_EACH_GESTURE * len(actions)}, {EACH_VIDEO_FRAME_LENGTH}, 126)"
    print(in_italics(f"Numpy Array for X (hand features), should be equal to {in_green(correct_videos_shape)}: "), end='')
    print(X.shape)  #should be (num_of_video * number of actions, video_length, num of features equal to (the shape of results) all key points identified by mediapipe in each frame)
    correct_labels_shape = f"({NUMBER_OF_VIDEOS_FOR_EACH_GESTURE * len(actions)},)"
    print(in_italics(f"Numpy Array for y (labels), should be equal to {in_green(correct_labels_shape)}: "), end='')
    print(np.array(labels).shape)  #should be num_of_video * number of actions
    print(in_yellow("Compare with the highlighted output to see if you got it right!"))
    
    print("Splitting dataset into test and training datasets ...",end='')
    try:
        from global_variables.user_specific import TRAINING_TEST_SPLIT
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TRAINING_TEST_SPLIT)
        issue_success()
    except:
        issue_failure()
        print(in_red(f"Something went wrong trying to split the data into test dataset by {TRAINING_TEST_SPLIT*100}%"))
        exit()    
    
    print("Creating model with given parameters ... ",end='')
    try:
        model = build_neural_network(EACH_VIDEO_FRAME_LENGTH, 126, len(actions))
        issue_success()
    except:
        issue_failure()
        print(in_red("Something went wrong trying to build the neural network!!"))
        exit()

    print("Training the built neural network using the training and test datasets .... ")
    from global_variables.user_specific import NUM_OF_EPOCHS
    import os
    from keras.callbacks import TensorBoard
    from global_variables.user_specific import LOGGER_FOLDER_NAME
    log_dir = os.path.join(LOGGER_FOLDER_NAME)
    tb_callback = TensorBoard(log_dir=log_dir)
    model.fit(X_train, y_train, epochs=NUM_OF_EPOCHS, callbacks=[tb_callback])
    model.summary()

    model_name = ask_for_model_name()
    from global_variables.user_specific import MODEL_SAVE_LOCATION
    print(f"Saving the model into the {MODEL_SAVE_LOCATION} ... ")
    try:
        model.save(f'../{DATA_FOLDER}/{MODEL_SAVE_LOCATION}/{model_name}{model_extension}')
        issue_success()
    except:
        issue_failure()
        print(in_yellow(f"Couldn't save {model_name}{model_extension}, something terrible happened!"))

def load_model(num_of_actions, model_name):
    model = build_neural_network(EACH_VIDEO_FRAME_LENGTH, num_of_actions)
    model.load_weights(f'{models_loc}/{model_name}{model_extension}')
    return model

def prob_viz(res, actions, input_frame, colors):
    import cv2
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    return output_frame

def test_from_camera_feed():

    no_models_to_test, _ = get_all_trained_models()
    
    if no_models_to_test == True:
        print(in_red("You do not have any models to test, I'm sorry !"))
        return
    
    from gestures_functions import load_gestures
    actions = load_gestures()
    print(in_italics("Fetched gestures from storage!"))
    
    print_all_trained_models()

    model_name = ask_for_model_name()
    print(in_bold(f"Loading {model_name}{model_extension} from existing models in {models_loc}"))
    try:
        model = load_model(len(actions), model_name)
        issue_success()
    except:
        issue_failure()
        print(in_red("Something went wrong trying to load model from storage!"))
        exit()

    import cv2
    import numpy as np

    # 1. New detection variables
    sequence = []
    current_command = ''
    history = []
    predictions = []
    threshold = 0.85

    # Mediapipe variables
    from mediapipe_functions import get_mediapipe_variables, mediapipe_detection, draw_styled_landmarks, extract_keypoints
    mp_holistic, _ = get_mediapipe_variables()

    from global_variables.user_specific import WINDOW_NAME, CAMERA_FEED_EXIT_CHAR, CAMERA_NUMBER

    feed = cv2.VideoCapture(CAMERA_NUMBER)
    # Set mediapipe model 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while feed.isOpened():

            # Read feed
            ret, frame = feed.read()

            # Exit camera feed if feed cannot be read
            if ret == False:
                print(in_red("Camera feed not accesible"))
                break

            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            # print(results)
            
            # Draw landmarks
            draw_styled_landmarks(image, results)
            
            # 2. Prediction logic
            keypoints = extract_keypoints(results, should_print=False)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            image = cv2.flip(image, 1)
            
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(in_green(actions[np.argmax(res)]+"- Probability: "+str(round(np.max(res)*100,2))+"%"))
                predictions.append(np.argmax(res))
                
                
            #3. Viz logic
                if np.unique(predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > threshold: 
                        
                        current_command = actions[np.argmax(res)]

                        if len(history) > 0: 
                            if actions[np.argmax(res)] != history[-1]:
                                history.append(actions[np.argmax(res)])
                        else:
                            history.append(actions[np.argmax(res)])

                if len(history) > 5: 
                    history = history[-5:]

                # Viz probabilities
                image = prob_viz(res, actions, image, colors)

            cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
            cv2.putText(image, ' '.join(history), (3,30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'Current command: ' + current_command, (3,240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Show to screen
            cv2.imshow(WINDOW_NAME, image)

            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord(CAMERA_FEED_EXIT_CHAR):
                break

        feed.release()
        cv2.destroyAllWindows()

def get_all_trained_models():
    no_models_to_test, existing_models = is_dir_empty(models_loc)
    return no_models_to_test, existing_models

def print_all_trained_models():
    no_models_to_test, existing_models = get_all_trained_models()
    if no_models_to_test == True:
        print(in_red("You have no trained models currently stored in the project!"))
    else:
        print(in_green("Found exisiting models:"))
        for model in existing_models:
            print(in_bold(model))

def main():
    choice = 0
    while(choice!=9):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("List of actions related to the stored dataset: ")
        print("1. Print the available trained models and their summary.")
        print(f"2. Train a new model with the current dataset and save it in {models_loc}")
        print(f"3. Test an existing model in the {models_loc}")
        print("9. Exit program")
        choice = int(input(in_bold("Choice: ")))
        if choice == 1:
            print_all_trained_models()
        elif choice == 2:
            train_model_on_data()
        elif choice == 3:
            test_from_camera_feed()
        elif choice == 9:
            break
        if input("Continue (Y/N): ").upper() == 'Y':
            continue
        else:
            break

if __name__ == '__main__':
    main()

