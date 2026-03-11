import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib


from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import os
import json

def create_recursive_data(df, wd_size=5):
    for i in range(1, wd_size):
        df[f"totalAmount_{i}"] = df["totalAmount"].shift(-i)
    df["target"] = df["totalAmount"].shift(-wd_size)
    return df.dropna()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "orders.csv")

# ✅ ĐÚNG ENCODING
df = pd.read_csv(csv_path, encoding="utf-8-sig")

df["orderDate"] = pd.to_datetime(df["orderDate"])
df["totalAmount"] = pd.to_numeric(df["totalAmount"], errors="coerce")
df["totalAmount"] = df["totalAmount"].interpolate()

df = create_recursive_data(df)

X = df.drop(["target", "orderDate"], axis=1)
y = df["target"]

train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

joblib.dump({"model": model},   "linear_regression.joblib")
data = joblib.load("linear_regression.joblib")
model = data["model"]
last_5_days = df.tail(5)["totalAmount"].values
X_future = pd.DataFrame([{
    "totalAmount": last_5_days[0],
    "totalAmount_1": last_5_days[1],
    "totalAmount_2": last_5_days[2],
    "totalAmount_3": last_5_days[3],
    "totalAmount_4": last_5_days[4]
}])
tomorrow_pred = model.predict(X_future)[0]

result = {
    "MAE": float(mean_absolute_error(y_test, y_pred)),
    "MSE": float(mean_squared_error(y_test, y_pred)),
    "RMSE": float(np.sqrt(mean_squared_error(y_test, y_pred))),
    "R2": float(r2_score(y_test, y_pred)),
    "Tomorrow_Prediction": float(round(tomorrow_pred, 2))

}

print(json.dumps(result))

plt.figure(figsize=(10, 5))
plt.plot(df["orderDate"][:train_size], df["totalAmount"][:train_size], label="Doanh thu huấn luyện")
plt.plot(df["orderDate"][train_size:], df["totalAmount"][train_size:], label="Doanh thu thực tế")
plt.plot(df["orderDate"][train_size:], y_pred, label="Doanh thu dự đoán")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "output.png"))
plt.close()
