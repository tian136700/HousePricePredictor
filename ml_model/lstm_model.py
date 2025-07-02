import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def create_dataset(series, window_size):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i+window_size])
        y.append(series[i+window_size])
    return np.array(X), np.array(y)

def train_lstm_model(data, window_size=12, epochs=100):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    X, y = create_dataset(data_scaled, window_size)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = tf.keras.Sequential([
        tf.keras.Input(shape=(window_size, 1)),
        tf.keras.layers.LSTM(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=epochs, verbose=0)

    return model, scaler
