import pandas as pd
import altair as alt
import streamlit as st
import yfinance as yf


def get_target_tickers(tickers: dict, companies: list) -> dict:
    target = {key: val 
            for key, val in tickers.items() 
            for c in companies if key == c}
    return target

@st.cache_data
def get_data(tickers: dict, days: int=20, sort: bool = True) -> pd.DataFrame:
    df = pd.DataFrame()

    for key, symbol in tickers.items():
        # ティッカーシンボル指定
        tkr = yf.Ticker(symbol)
        hist = tkr.history(period=f'{days}d')
        hist.head()
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [key]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    
    if sort: df = df.sort_index()
    return df

def shaping_data(data: pd.DataFrame) -> pd.DataFrame:
    """       day1 | day2 | day3
    company1 | 1   | 2    | 3
    company2 | 1   | 2    | 3
    
    ↓に変形

    Date | name     | Stock Prices(USD)
    1    | company1 | 1
    2    | company1 | 2
    3    | company1 | 3
    1    | company2 | 1
    2    | company2 | 2
    3    | company2 | 3

    """
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date'])
    data = data.rename(columns={'value': 'Stock Prices(USD)'})

    return data


def drawing(data: pd.DataFrame, y_min: float, y_max: float) -> alt.Chart:
    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8)
        .encode(
            x="Date:T",
            y=alt.Y(
                "Stock Prices(USD):Q", 
                stack=None, 
                scale=alt.Scale(domain=[y_min, y_max])),
            color='Name:N'
        )
    )
    return chart