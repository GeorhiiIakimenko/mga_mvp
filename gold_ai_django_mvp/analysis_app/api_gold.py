import requests
import pandas as pd

api_key = '1LIUUC0LBOCFOJ9P'
symbol = 'XAUUSD'  # Символ для золота

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

response = requests.get(url)
data = response.json()

# Преобразование данных в DataFrame
df = pd.DataFrame(data['Time Series (Daily)']).T
df.reset_index(inplace=True)
df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

# Фильтрация данных за последние три года
three_years_ago = pd.to_datetime('today') - pd.DateOffset(years=3)
df['Date'] = pd.to_datetime(df['Date'])
filtered_df = df[df['Date'] >= three_years_ago]

# Сохранение данных в CSV
filtered_df.to_csv('gold_prices_alpha_vantage.csv', index=False)
