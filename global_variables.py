# Virtial Environment name
virtual_env_name = 'my-project-env'

# My PC had two cameras, back and front, so for front camera, the number was 1
# Please edit this according to your system for the correct camera device number
camera_number = 1

# Camera feed related settings
window_name = 'Webcam feed'
camera_feed_exit_char = 'q'

# Training data related settings
training_data_folder_name = 'training_action_data'
number_of_videos_for_each_gesture = 30
each_video_frame_length = 30

# Wait time before every video collection for every action (frame 0 for every video)
frame_collection_wait_time = 2000 #milliseconds

# Model training related settings
logger_folder_name = 'logs'
num_of_epochs = 2000