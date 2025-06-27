# 房价预测系统（House Price Predictor）

## 项目简介
本项目实现了一个基于机器学习的房价预测系统。用户通过网页输入房屋信息，系统基于历史数据预测房价，并展示历史价格走势图。后端使用 Flask，模型采用 scikit-learn 线性回归，前端为简单的 HTML 页面。

## 目录结构
```
房价预测系统/
├── app.py                     # Flask 后端主程序
├── train_model.py             # 模型训练脚本
├── house_price_model.pkl      # 训练好的模型文件
├── house_prices.csv           # 房价数据CSV文件
├── requirements.txt           # 依赖库列表
├── templates/
│   └── index.html             # 前端页面
├── static/
│   ├── css/
│   │   └── style.css          # 样式文件（可选）
│   └── js/
│       └── main.js            # 脚本文件（可选）
├── README.md                  # 项目说明文件
└── .gitignore                 # Git忽略文件
```

## 环境依赖
建议使用 Python 3.7 及以上版本，安装依赖：

```bash
pip install -r requirements.txt
```

requirements.txt 示例内容：

```
pandas
scikit-learn
joblib
matplotlib
flask
```

## 运行步骤

1. **准备数据**  
   确保 `house_prices.csv` 文件在项目根目录，数据应包含 `area`,  `city`, `price`, `year` 等字段。

2. **训练模型**  
   运行训练脚本：

   ```bash
   python train_model.py
   ```

   会生成 `house_price_model.pkl` 模型文件。

3. **启动后端服务**  
   运行 Flask 应用：

   ```bash
   python app.py
   ```

   默认监听地址为 `http://127.0.0.1:5000`。

4. **访问前端页面**  
   用浏览器打开 `http://127.0.0.1:5000`，输入房屋信息进行预测。

## 注意事项
- 请确保模型文件 `house_price_model.pkl` 与 `app.py` 在同一目录，且模型文件完整有效。  
- 修改数据文件或字段时需同步修改代码。  
- 项目仅为学习演示，实际项目可根据需求扩展更多功能。  

---

欢迎提出建议和反馈！
