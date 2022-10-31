import time  
import numpy as np  
import pandas as pd  
import plotly.express as px 
import plotly.graph_objects as go
import streamlit as st  
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from src.config import Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY
##### streamlit run .\src\tests.py

# This is a quick streamlit webapp I 
# created to easily monitor the 3 accounts
# I am comparing and create visualizations
# for better insights into each accounts'
# activity and success/failure.

st.set_page_config(
    page_title="RAM Trading Bot Dashboard",
    page_icon="💰",
    layout="wide",
)
# Alpaca Accounts
r_trading_client = TradingClient(Reddit_ALPACA_API_KEY, Reddit_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
r_stock_client = StockHistoricalDataClient(Reddit_ALPACA_API_KEY,  Reddit_ALPACA_SECRET_KEY)
# r_account = r_trading_client.get_account()

a_trading_client = TradingClient(Algo_ALPACA_API_KEY, Algo_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
a_stock_client = StockHistoricalDataClient(Algo_ALPACA_API_KEY,  Algo_ALPACA_SECRET_KEY)
# a_account = a_trading_client.get_account()

m_trading_client = TradingClient(Neural_ALPACA_API_KEY, Neural_ALPACA_SECRET_KEY, paper=True) # each has different keys since they are on different accounts
m_stock_client = StockHistoricalDataClient(Neural_ALPACA_API_KEY,  Neural_ALPACA_SECRET_KEY)
# m_account = m_trading_client.get_account()

# dashboard title
st.title("R.A.M. Trading Realtime Data Dashboard")

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation
while True:
    aliases = {
    "Reddit" : r_trading_client.get_all_positions(),
    "Algo" : a_trading_client.get_all_positions(),
    "Neural" : m_trading_client.get_all_positions()
    }
    columns = [
        'Ticker',
        'Current Price',
        'Last Close Price',
        'Price Change',
        'Quantity',
        'Average Price',
        'Cost Basis',
        'Market Value',
        'Profit/Loss',
        'Profit/Loss %'
    ]
    dataframes_positions = {}
    acc_df = pd.read_csv("C:/trading_bot/src/acc_data.csv") 
    for client in aliases.keys():
        stock_df = pd.DataFrame(columns = columns)
        appender = []
        try:    
            for stock in aliases[client]:
                df_new_row = pd.Series(
                    [
                        stock.symbol,
                        f'{float(stock.current_price): .2f}',
                        f'{float(stock.lastday_price): .2f}',
                        f'{float(stock.change_today) * 100: .2f}',
                        int(stock.qty),
                        f'{float(stock.avg_entry_price): .2f}',
                        f'{float(stock.cost_basis): .2f}',
                        f'{float(stock.market_value): .2f}',
                        f'{float(stock.unrealized_pl): .2f}',
                        f'{float(stock.unrealized_plpc) * 100: .2f}'
                    ], 
                    index=columns
                ) 
                appender.append(df_new_row)
            stock_df = pd.concat(appender, axis=1, ignore_index=True).T
        except:
            continue

        total = stock_df['Cost Basis'].astype(float).sum()
        perc_column = []
        for i in range(0, len(stock_df)):
            value = (float(stock_df['Cost Basis'].iloc[i]) / total) * 100
            perc_column.append(f'{value: .2f}')
        stock_df["Stock % of Portfolio"] = perc_column
        stock_df["Color"] = np.where(stock_df["Profit/Loss"].astype(float)<0, 'red', 'green')

        dataframes_positions[client] = stock_df

    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Reddit Account Value 🤮",
            value=f"$ {round(float(r_trading_client.get_account().portfolio_value),2)} ",
            delta=round(float(r_trading_client.get_account().portfolio_value) - 500000, 2)
        )
        
        kpi2.metric(
            label="Algo Account Value 🔢",
            value=f"$ {round(float(a_trading_client.get_account().portfolio_value),2)} ",
            delta=round(float(a_trading_client.get_account().portfolio_value) - 500000, 2)
        )
        
        kpi3.metric(
            label="Neural Account Value 🧠",
            value=f"$ {round(float(m_trading_client.get_account().portfolio_value),2)} ",
            delta=round(float(m_trading_client.get_account().portfolio_value) - 500000, 2)
        )

        # create three columns
        kpi4, kpi5, kpi6 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi4.metric(
            label="Reddit Account Buying Power 🤮",
            value=f"$ {round(float(r_trading_client.get_account().buying_power),2)} ",
            delta=round(float(r_trading_client.get_account().buying_power) - 1000000, 2)
        )
        
        kpi5.metric(
            label="Algo Account Buying Power 🔢",
            value=f"$ {round(float(a_trading_client.get_account().buying_power),2)} ",
            delta=round(float(a_trading_client.get_account().buying_power) - 1000000, 2)
        )
        
        kpi6.metric(
            label="Neural Account Buying Power 🧠",
            value=f"$ {round(float(m_trading_client.get_account().buying_power),2)} ",
            delta=round(float(m_trading_client.get_account().buying_power) - 1000000, 2)
        )

        # create two columns for charts
        fig_col1, fig_col2, fig_col3 = st.columns(3)
        with fig_col1:
            st.markdown("### Reddit Daily Chart")
            fig = px.line(acc_df, x="Date", y="Reddit Account Value")
            st.write(fig)
            
        with fig_col2:
            st.markdown("### Algo Daily Chart")
            fig2 = px.line(acc_df, x="Date", y="Algo Account Value")
            st.write(fig2)
        
        with fig_col3:
            st.markdown("### Neural Daily Chart")
            fig3 = px.line(acc_df, x="Date", y="Neural Account Value")
            st.write(fig3)

        try:
            fig_col4, fig_col5 = st.columns(2)
            with fig_col4:
                st.markdown("### Reddit Positions Distributions")
                fig4 = px.pie(dataframes_positions["Reddit"], values="Stock % of Portfolio", names="Ticker")
                st.write(fig4)
                
            with fig_col5:
                st.markdown("### Reddit Positions Profit/Loss")
                fig5 = go.Figure()
                fig5.add_trace(
                    go.Bar(
                        x=dataframes_positions["Reddit"]["Ticker"],
                        y=dataframes_positions["Reddit"]["Profit/Loss"].astype(float),
                        marker_color=dataframes_positions["Reddit"]["Color"],
                        base=0))
                fig5.update_layout(barmode='stack')
                st.write(fig5)


            fig_col6, fig_col7 = st.columns(2)
            with fig_col6:
                st.markdown("### Algo Positions Distributions")
                fig6 = px.pie(dataframes_positions["Algo"], values="Stock % of Portfolio", names="Ticker")
                st.write(fig6)
                
            with fig_col7:
                st.markdown("### Algo Positions Profit/Loss")
                fig7 = go.Figure()
                fig7.add_trace(
                    go.Bar(
                        x=dataframes_positions["Algo"]["Ticker"],
                        y=dataframes_positions["Algo"]["Profit/Loss"].astype(float),
                        marker_color=dataframes_positions["Algo"]["Color"],
                        base=0))
                fig7.update_layout(barmode='stack')
                st.write(fig7)

            fig_col8, fig_col9 = st.columns(2)
            with fig_col8:
                st.markdown("### Neural Positions Distributions")
                fig8 = px.pie(dataframes_positions["Neural"], values="Stock % of Portfolio", names="Ticker")
                st.write(fig8)
                
            with fig_col9:
                st.markdown("### Neural Positions Profit/Loss")
                fig9 = go.Figure()
                fig9.add_trace(
                    go.Bar(
                        x=dataframes_positions["Neural"]["Ticker"],
                        y=dataframes_positions["Neural"]["Profit/Loss"].astype(float),
                        marker_color=dataframes_positions["Neural"]["Color"],
                        base=0))
                fig9.update_layout(barmode='stack')
                st.write(fig9)
            
            


            st.markdown("### Reddit Account Positions")
            st.dataframe(dataframes_positions["Reddit"])
            st.markdown("### Algo Account Positions")
            st.dataframe(dataframes_positions["Algo"])
            st.markdown("### Neural Account Positions")
            st.dataframe(dataframes_positions["Neural"])
        except:
            continue
        time.sleep(1)