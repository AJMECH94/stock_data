import typer
import requests
import pandas as pd
import numpy as np

app = typer.Typer()
api_key = "ND6S6BGBJAZH4MZU"

@app.command()
def process_stock_data(symbol: str, start_date: str, end_date: str):
    try:
        if symbol:
            # Retrieve data from API
            # if period=='day':
            #     url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full"
            #     response = requests.get(url)
            #     data = response.json()["Time Series (Daily)"]
            # elif period=='week':
            #     print("week")
            #     url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full"
            #     response = requests.get(url)
            #     data = response.json()["Weekly Adjusted Time Series"]
            # elif period=='month':
            # print("month")
            url = url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full"
            response = requests.get(url)
            data = response.json()["Time Series (Daily)"]
            stock_data = pd.DataFrame(data)
            stock_data = stock_data.transpose()
            stock_data = stock_data.rename(columns={
                '1. open': 'open',
                '2. high' : 'high',
                '3. low' : 'low',
                '4. close' : 'close',
                '5. adjusted close' : 'adjusted close',
                '6. volume' : 'volume',
                '7. dividend amount': 'dividend amount',
                '8. split coefficient': 'split coefficient'
                })
            
            stock_data['adjusted close'] = stock_data['adjusted close'].astype(float)
            stock_data = stock_data[(stock_data.index >= start_date) & (stock_data.index <= end_date)]
            print(stock_data)
            daily_returns = stock_data['adjusted close'].pct_change()
            total_return = (stock_data['adjusted close'][-1] - stock_data['adjusted close'][0]) / stock_data['adjusted close'][0]
            annualized_return = ((1 + daily_returns.mean()) ** 252) - 1
            volatility = daily_returns.std() * np.sqrt(252)
            risk_free_rate = 0.02
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility
            results = pd.DataFrame({
                'Total Return': [total_return],
                'Annualized Return': [annualized_return],
                'Volatility': [volatility],
                'Sharpe Ratio': [sharpe_ratio]
            })
            print(results)
            results.to_csv('mydata.csv', index=False)
        else:
            print("please enter a valid symbol")
    except Exception as msg:
        print("Enter valid symbol")


if __name__ == "__main__":
    app()