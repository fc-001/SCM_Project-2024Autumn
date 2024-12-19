import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

data = pd.read_excel("YongHuiFreshRevenue.xlsx")
data['date'] = pd.to_datetime(data['时间'])
data = data[['营业额(万元)']]
data['营业额(万元)'] = (
    data['营业额(万元)']
    .astype(str)
    .str.replace(',', '')
    .astype(float)
)

train_data = data.iloc[:-4]
test_data = data.iloc[-4:]

# SARIMA
sarima_order = (1, 1, 1)
seasonal_order = (1, 1, 1, 2)
sarima_model = SARIMAX(train_data['营业额(万元)'], order=sarima_order, seasonal_order=seasonal_order)
sar_res = sarima_model.fit()
sar_pre = sar_res.forecast(steps=len(test_data))
sar_r = test_data['营业额(万元)'] - sar_pre
scaler = MinMaxScaler()
norm_sar = scaler.fit_transform(sar_r.values.reshape(-1, 1))

timesteps = 1
X_train = np.array([norm_sar[i:i + timesteps] for i in range(len(norm_sar) - timesteps)])
y_train = norm_sar[timesteps:]

# LSTM
lstm_model = Sequential([
    LSTM(50, activation='tanh', return_sequences=True, input_shape=(timesteps, 1)),
    Dropout(0.2),
    LSTM(50, activation='tanh', return_sequences=False),
    Dropout(0.2),
    Dense(1)
])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=0)
X_test = np.array([norm_sar[-timesteps:]])
lstm_pre = lstm_model.predict(X_test)
lstm_res = scaler.inverse_transform(lstm_pre)

# 组合预测
res = sar_pre.values + lstm_res.flatten()
test_data.index = ['22-12', '23-6', '23-12', '24-6']
mse = mean_squared_error(test_data['营业额(万元)'], res)
mae = mean_absolute_error(test_data['营业额(万元)'], res)
mape = (np.mean(np.abs((test_data['营业额(万元)'] - res) / test_data['营业额(万元)'])) * 100)

# 可视化
fig, ax = plt.subplots(figsize=(15, 9))
plt.ticklabel_format(style='plain', axis='y')
plt.plot(test_data.index, test_data['营业额(万元)'], label="Real Value", marker='o')
plt.plot(test_data.index, res, label="Prediction Value", marker='x')
plt.legend()
plt.title("SARIMA-LSTM Result")
ax.set_title("SARIMA-LSTM Result", fontsize=16)
ax.set_ylabel("REVENUE(10^5)", fontsize=12)
ax.set_xlabel("DATE", fontsize=12)
ax.legend(fontsize=12)
ax.grid(True)
plt.figtext(0.5, 0.01, f"MSE: {mse:.4f}, MAE: {mae:.4f}, MAPE: {mape:.4f}%", fontsize=12, ha="center")
plt.show()