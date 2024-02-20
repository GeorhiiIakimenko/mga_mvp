import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

# Download historical data for an adjusted time period
ticker = "GLD"
data = yf.download(ticker, start="2023-01-01", end="2023-12-31")
data['Price_Difference'] = data['Close'].diff()
data = data.dropna()

data = data.copy()

data.loc[:, 'Price_Direction'] = (data['Price_Difference'] > 0).astype(int)

# Define target variable and features
X = data[['Open', 'High', 'Low', 'Close', 'Volume']]
y = data['Price_Direction']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create and train logistic regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Make probability predictions on the test set
y_proba = model.predict_proba(X_test_scaled)

# Evaluate model performance using probabilities
# You can use probabilities to make more nuanced decisions based on your criteria
# For example, you might classify as 'Up' if the probability of 'Up' is greater than 0.5
# and 'Down' otherwise
y_pred_prob = (y_proba[:, 1] > 0.5).astype(int)

# Evaluate model performance
accuracy = metrics.accuracy_score(y_test, y_pred_prob)
print(f'Accuracy: {accuracy}')

# Make probability predictions for a future period
future_data = yf.download(ticker, start="2024-01-01", end="2024-02-01")
future_data['Price_Difference'] = future_data['Close'].diff()
future_data = future_data.dropna()

# Scale the features for future predictions
future_features_scaled = scaler.transform(future_data[['Open', 'High', 'Low', 'Close', 'Volume']])
future_predictions_proba = model.predict_proba(future_features_scaled)

# Set a threshold for classifying as 'Up'
threshold = 0.5

# Convert probabilities to arrows (Up or Down)
future_predictions_arrows = ['↑' if prob[1] > threshold else '↓' for prob in future_predictions_proba]

print("Predictions for future price movement:")
print(future_predictions_arrows)
