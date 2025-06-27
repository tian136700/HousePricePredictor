import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


# 读取数据（你要换成自己的数据路径）
data = pd.read_csv('house_prices.csv')  # 示例文件名

# 简单查看数据结构
print(data.head())

# 选择特征和目标（假设数据中有：area, bedrooms, city, price）
features = ['area', 'bedrooms', 'city']
target = 'price'

X = data[features]
y = data[target]

# 分类变量编码
categorical_features = ['city']
numerical_features = ['area', 'bedrooms']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
    ], remainder='passthrough')

# 建立回归管道
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# 划分训练测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model.fit(X_train, y_train)

# 评估（简单输出）
score = model.score(X_test, y_test)
print(f'Model R^2 score: {score:.4f}')

# 保存模型
joblib.dump(model, 'house_price_model.pkl')
print('Model saved as house_price_model.pkl')
