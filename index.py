import streamlit as st
import pandas as pd
import yfinance as yf
from yahoo_fin import stock_info
import cufflinks as cf

# |********* Trading Dashboard with SMA, EMA, ADX, MACD, Boilinger Bands indicators *********|

# Page configuration
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="👾",
    layout="wide",
) 

# Sidebar with indicator settings
with st.sidebar:
    st.header('Stock Dashboard')

    stock_name_input = st.text_input(label='Stock or Crypto Ticker ("Ticker-USD" format for crypto)', value='eth-usd', placeholder='Enter the ticker', type="default")

    col1, col2 = st.columns(2)
    with col1:
        sma = st.number_input('SMA', 0, 200, value=14)
    with col2:
        ema = st.number_input('EMA', 0, 200, value=14)

    adx = st.number_input('ADX', 0, 200, value=14)

    st.write('Boilinger Bands')
    col5, col6 = st.columns(2)
    with col5:
        bb_periods = st.number_input('Periods', 0, 200)
    with col6:
        bb_sd = st.number_input('Standard Deviation', 0, 200)

    stock_name = yf.Ticker(stock_name_input)
    stock_data = stock_info.get_data(stock_name_input, start_date="04/12/2021", index_as_date = True)

    ticker_data = ['country', 'market', 'sector', 'industry', 'fullTimeEmployees', 'marketCap',
               'returnOnEquity', 'freeCashflow', 'priceToBook', 'dividendYield', 
               'dividendRate', 'beta']
    company_details = dict([[key,value] for key, value in stock_name.info.items() if key in ticker_data])

    st.text("Brief info about the company:")
    st.write(company_details)

# Define the chart
qf = cf.QuantFig(stock_data, kind='candlestick', legend='top', theme='solar', title=stock_name.info['shortName'])

qf.add_volume()

rangeselector=dict(steps=['ALL','3Y','2Y','1Y','YTD','6M','1M','1MTD'], bgcolor=('#000'), 
                   fontsize=12, fontfamily='monospace')

# Adding SMA to the figure
qf.add_sma(periods=sma, color='yellow')

# Adding EMA to the figure
qf.add_ema(periods=ema, color='cyan')

# Adding Boilinger Bands to the figure
qf.add_bollinger_bands(periods=bb_periods, boll_std=bb_sd, colors=['magenta','orange'], fill=True)

# Adding ADX to the figure
qf.add_adx(periods=adx)

# Adding RSI to the figure. Keep in mind that more adding more indicators will overpopulate the plot.
#qf.add_rsi(periods=rsi, rsi_upper=70, rsi_lower=30, showbands=True)
# Add MACD
qf.add_macd()
qf.layout.update(rangeselector=rangeselector)
st.plotly_chart(qf.iplot(up_color='blue', down_color='red', rangeslider=False, asFigure=True, dimensions =(950,850)))

# News table
st.subheader('News')
try:
    st.dataframe(pd.DataFrame(stock_name.news, columns=['title', 'publisher', 'link', 'type']))
except:
    st.write('No news found 👀')

# Hide the footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)