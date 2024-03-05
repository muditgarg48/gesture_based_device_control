from scripts.commandline_functions import *
from global_variables.user_specific import EACH_VIDEO_FRAME_LENGTH
from global_variables.user_specific import MODEL_SAVE_LOCATION

colors = [(245,117,16), (117,245,16), (16,117,245)]
model_extension = '.h5'

def ask_for_model_name():
    print_in_yellow("You do not need to mention the extension of the model!!")
    model_name = input(f"Enter the name of the existing model to be tested from {MODEL_SAVE_LOCATION}:")
    if model_name[-3:] == model_extension:
        print_in_yellow(f"Its useless to type {model_extension} as well!!")
        model_name = model_name[:-3]
    return model_name

def load_model(num_of_frames, num_of_features, num_of_actions, model_name):
    from scripts.build_model import build_neural_network
    model = build_neural_network(num_of_frames, num_of_features, num_of_actions)
    model.load_weights((f'./{MODEL_SAVE_LOCATION}/{model_name}{model_extension}'))
    return model

def get_num_of_actions():
    from scripts.gestures_functions import get_num_of_gestures
    return get_num_of_gestures()

def get_actions():
    from scripts.gestures_functions import load_gestures
    return load_gestures()

def prob_viz(res, actions, input_frame, colors):
    import cv2
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    return output_frame

def test_from_camera_feed(model, actions):

    import cv2
    import numpy as np

    # 1. New detection variables
    sequence = []
    current_command = ''
    history = []
    predictions = []
    threshold = 0.8

    # Mediapipe variables
    from scripts.mediapipe_functions import get_mediapipe_variables, mediapipe_detection, draw_styled_landmarks, extract_keypoints
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
                print_in_red("Camera feed not accesible")
                break

            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            print(results)
            
            # Draw landmarks
            draw_styled_landmarks(image, results)
            
            # 2. Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            image = cv2.flip(image, 1)
            
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions[np.argmax(res)])
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

def main(num_of_frames=EACH_VIDEO_FRAME_LENGTH, num_of_features=126):
    do_we_have_models_to_test, existing_models = is_dir_empty(MODEL_SAVE_LOCATION)
    if do_we_have_models_to_test == True:
        print_in_red("You have no trained models currently stored in the project!")
        print_in_bold("Train some models to test them!")
        exit()
    else:
        print_in_green("Found exisiting models:")
        for model in existing_models:
            print_in_italics(model)
        print()
    model_name = ask_for_model_name()
    print_in_bold("Fetching the gesture data from storage ...")
    print_in_bold("==========================================")
    num_of_actions = get_num_of_actions()
    print_in_italics("Fetched number of gestures stored!")
    actions = get_actions()
    print_in_italics("Fetched all the gestures stored!")
    print_in_bold(f"Loading {model_name}{model_extension} from existing models in {MODEL_SAVE_LOCATION} ...")
    print_in_bold("==========================================================================")
    model = load_model(num_of_frames, num_of_features, num_of_actions, model_name)
    print_in_bold("Opening testing camera feed ...")
    print_in_bold("===============================")
    test_from_camera_feed(model, actions)

if __name__ == '__main__':
    main()