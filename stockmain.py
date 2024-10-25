import streamlit as sl 
import datetime
import yfinance as yf 
from prophet import Prophet
#from fbprophet.plot import plot_plotly
import plotly.figure_factory as ff
from plotly import graph_objs as go 
from tickerdetails import get_ticker
import pandas as pd 
import matplotlib.pyplot as plt
from prophet.plot import plot_plotly, plot_components_plotly

TODAY = datetime.date.today()

START = datetime.date.today() - datetime.timedelta(days=10*365)

sl.sidebar.title("Forecast Buddy")

result = get_ticker()

stocksname= result
selected_stock =sl.sidebar.selectbox("Select stock", stocksname)

years = sl.sidebar.slider("Years of forecast" , 1, 10)

period = years * 365

@sl.cache_data
def load_stock_data(stockname):
    data = yf.download(stockname,START,TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = sl.text("Load Stock Data")
data = load_stock_data(selected_stock)
data_load_state.text("Load completed")

basedatatab, basedatacharttab = sl.tabs(["🗃 Data" , "📈 Chart"])
basedatatab.subheader("Base Data")
basedatatab.write(data.tail())

basedatacharttab.subheader("Chart")
figure = go.Figure()
figure.add_trace(go.Scatter(x=data['Date'], y=data['High'], name='Ticker Open'))
figure.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name='Ticker Close'))
figure.layout.update(title_text="Time Data", xaxis_rangeslider_visible=True)
basedatacharttab.plotly_chart(figure)

dataframretraining = data[["Date","Close"]]
dataframretraining = dataframretraining.rename(columns={"Date": "ds", "Close": "y"})

model= Prophet()
model.fit(dataframretraining)
futuredata= model.make_future_dataframe(periods=period)
forecastdata = model.predict(futuredata)

sl.subheader("Forecast Data")
sl.write(forecastdata.tail())

model.plot(forecastdata)

#Download the Data for Ticker
sl.subheader("Summary")
sl.download_button("Download ticker Data", forecastdata.to_csv(index=True),file_name=f"{selected_stock}_TickerData.csv", mime="text/csv")

forecast_fig = plot_plotly(model, forecastdata)
forecast_component = plot_components_plotly(model, forecastdata)

forecasttab, componenttab = sl.tabs(["🗃 Forecast" , "📈 Componenets"])
forecasttab.subheader("Forecast")
forecasttab.write(forecast_fig)

componenttab.subheader("Forecast Componenets")
componenttab.write(forecast_component)