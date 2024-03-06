import cv2
import mediapipe_functions as mf
from global_variables.user_specific import CAMERA_NUMBER, WINDOW_NAME, CAMERA_FEED_EXIT_CHAR

def main():
    
    feed = cv2.VideoCapture(CAMERA_NUMBER)
    mp_holistic, _ = mf.get_mediapipe_variables()

    # This might not run sometimes, theres no bug, it just needs to be run again if the window opens and closes

    # Set mediapipe model and start the webcam
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic_model:
        while feed.isOpened():

            # Read image from the feed of the webcam
            return_value, frame = feed.read()

            if return_value == False:
                return 1

            # Make detections
            image, results = mf.mediapipe_detection(frame, holistic_model)
            # print(results)

            # Draw landmarks
            # draw_landmarks(image, results)
            mf.draw_styled_landmarks(image, results)

            image = cv2.flip(image, 1)
            
            cv2.imshow(WINDOW_NAME, image)

            if cv2.waitKey(10) & 0xFF == ord(CAMERA_FEED_EXIT_CHAR):
                break

        feed.release()
        cv2.destroyAllWindows()

    # Ability to disable and destroy all camera feeds and Open CV window instances
    feed.release()
    cv2.destroyAllWindows()

    return 0

if __name__ == '__main__':
    main()