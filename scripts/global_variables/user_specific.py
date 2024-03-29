# Project related settings
VIRTUAL_ENV_NAME = 'my-project-env'

# Please edit this according to your system for the correct camera device number
# If your system has two cameras, the front camera is 1 (most probably) and the back camera is 0 (most probably)
# If your system has one camera, the camera number is 1
# Try with other numbers if these do not work
CAMERA_NUMBER = 1

# Camera feed related settings
WINDOW_NAME = 'Webcam feed'
CAMERA_FEED_EXIT_CHAR = 'q'

# Training data related settings
DATA_FOLDER = 'data'
TRAINING_DATA_FOLDER_NAME = 'training_action_data'
MODEL_SAVE_LOCATION = 'models'
NUMBER_OF_VIDEOS_FOR_EACH_GESTURE = 30
EACH_VIDEO_FRAME_LENGTH = 30
TRAINING_TEST_SPLIT = 0.05

# Wait time before every video collection for every action (frame 0 for every video)
FRAME_COLLECTION_WAIT_TIME = 2000 #milliseconds

# Model training related settings
LOGGER_FOLDER_NAME = 'tensorboard_logs'
NUM_OF_EPOCHS = 200

USER_DEFINED_GLOBAL_VARS_PROJECT = {
    'VIRTUAL_ENV_NAME':VIRTUAL_ENV_NAME,
    'CAMERA_NUMBER': CAMERA_NUMBER,
    'WINDOW_NAME': WINDOW_NAME,
    'CAMERA_FEED_EXIT_CHAR': CAMERA_FEED_EXIT_CHAR,   
}