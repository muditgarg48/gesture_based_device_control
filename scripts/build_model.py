from keras.models import Sequential
from keras.layers import LSTM, Dense

def build_neural_network(num_of_frames, num_of_features, num_of_actions):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(num_of_frames, num_of_features)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(num_of_actions, activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

    return model