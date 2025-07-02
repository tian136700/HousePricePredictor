from flask import Blueprint, request, jsonify
from utils.data_loader import load_price_series
from ml_model.lstm_model import train_lstm_model
from ml_model.predictor import forecast_future
import pandas as pd

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict_prices', methods=['POST'])
def predict_prices():
    data = request.get_json()
    province = data.get('province')
    city = data.get('city')
    months = int(data.get('months', 12))  # 默认预测12个月

    if not province or not city:
        return jsonify({'error': '省份和城市不能为空'}), 400

    df = load_price_series(province, city)
    if df is None or df.empty:
        return jsonify({'error': '没有找到对应城市的房价数据'}), 404

    model, scaler = train_lstm_model(df.values)
    forecast = forecast_future(model, scaler, df.values, steps=months)

    last_date = df.index[-1]
    results = []
    for i, value in enumerate(forecast):
        future_date = last_date + pd.DateOffset(months=i+1)
        results.append({
            'year': future_date.year,
            'month': future_date.month,
            'predicted_price': round(float(value), 2)
        })

    return jsonify({
        'province': province,
        'city': city,
        'prediction': results
    })
