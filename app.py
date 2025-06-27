from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# 加载训练好的模型
model = joblib.load('house_price_model.pkl')

# 读取历史数据用于趋势图
historical_data = pd.read_csv('house_prices.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # 解析输入数据
    area = float(data['area'])
    bedrooms = int(data['bedrooms'])
    city = data['city']

    # 构造DataFrame传入模型
    input_df = pd.DataFrame([[area, bedrooms, city]], columns=['area', 'bedrooms', 'city'])
    pred_price = model.predict(input_df)[0]

    return jsonify({'predicted_price': round(pred_price, 2)})

@app.route('/price_trend')
def price_trend():
    # 简单绘制城市整体价格趋势折线图
    fig, ax = plt.subplots()
    # 按年份和城市平均房价（假设有 year 列）
    grouped = historical_data.groupby(['year', 'city'])['price'].mean().unstack()
    grouped.plot(ax=ax)
    plt.title('Historical Average House Prices by City')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.tight_layout()

    # 转换成图片流
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close(fig)
    return jsonify({'plot_url': f'data:image/png;base64,{plot_url}'})

if __name__ == '__main__':
    app.run(debug=True)
