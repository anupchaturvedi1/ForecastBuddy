import streamlit as sl 
import datetime

import yfinance as yf 
from prophet import Prophet
from plotly import graph_objs as go 
import pandas as pd 


TODAY = datetime.date.today()

print(TODAY)

year_to_minus = TODAY.year - 10

# START = TODAY.replace(year=year_to_minus).strftime("%Y-%m-%d")

START = "2015-01-02"

sl.title("Stock forecast")

stocksname= ("AAPL","GOOG","MSFT")

selected_stock = sl.selectbox("Select stock", stocksname)

years = sl.slider("Years of forecasrt" , 1, 10)

period = years * 365


def load_stock_data(stockname):
    data = yf.download(stockname,START,TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = sl.text("Load Stock Data")
data = load_stock_data(selected_stock)
data_load_state.text("Load completed")

sl.subheader("Data")
sl.write(data.tail())

print(data)

def plot_data():
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=data['Date'], y=data['High'], name='open'))
    figure.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name='close'))
    figure.layout.update(title_text="Time Data", xaxis_rangeslider_visible=True)
    sl.plotly_chart(figure)

plot_data()

dataframretraining = data[["Date","Close"]]
dataframretraining = dataframretraining.rename(columns={"Date": "ds", "Close": "y"})

model= Prophet()
model.fit(dataframretraining)

futuredata= model.make_future_dataframe(periods=period)

forecastdata = model.predict(futuredata)

sl.subheader("Forecast Data")
sl.write(forecastdata.tail())

model.plot(forecastdata)
# fig1 = plot_plotly(model, forecastdata)
# sl.plotly_chart(fig1)

sl.write("Forecast Components")
fig2 = model.plot_components(forecastdata)
sl.write(fig2)