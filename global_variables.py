# Project related settings
VIRTUAL_ENV_NAME = 'my-project-env'
PYTHON_MAJOR_VERSION_REQ = 3
PYTHON_MINOR_VERSION_REQ_MIN = 9
PYTHON_MINOR_VERSION_REQ_MAX = 11
REQUIRED_PACKAGES = [
    { "id": "cv2", "name": "OpenCV" },
    { "id": "numpy", "name": "Numpy" },
    { "id": "matplotlib", "name": "Matplotlib" },
    { "id": "mediapipe", "name": "Mediapipe" },
    { "id": "tensorflow", "name": "Tensorflow" },
    { "id": "keras", "name": "Keras" },
    { "id": "sklearn", "name": "Scikit Learn" },
]

# My PC had two cameras, back and front, so for front camera, the number was 1
# Please edit this according to your system for the correct camera device number
CAMERA_NUMBER = 1

# Camera feed related settings
WINDOW_NAME = 'Webcam feed'
CAMERA_FEED_EXIT_CHAR = 'q'

# Training data related settings
TRAINING_DATA_FOLDER_NAME = 'training_action_data'
NUMBER_OF_VIDEOS_FOR_EACH_GESTURE = 30
EACH_VIDEO_FRAME_LENGTH = 30

# Wait time before every video collection for every action (frame 0 for every video)
FRAME_COLLECTION_WAIT_TIME = 2000 #milliseconds

# Model training related settings
LOGGER_FOLDER_NAME = 'logs'
NUM_OF_EPOCHS = 2000