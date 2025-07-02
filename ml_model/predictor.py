import numpy as np

def forecast_future(model, scaler, data, window_size=12, steps=12):
    scaled_data = scaler.transform(data)
    last_window = scaled_data[-window_size:]

    predictions = []

    for _ in range(steps):
        input_seq = last_window.reshape((1, window_size, 1))
        next_value = model.predict(input_seq, verbose=0)[0][0]
        predictions.append(next_value)
        last_window = np.append(last_window[1:], [[next_value]], axis=0)

    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
