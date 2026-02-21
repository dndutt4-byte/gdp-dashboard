import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Udbhav AI Trader", layout="wide")
st.title("📊 Udbhav AI: कैंडलस्टिक बाय-सेल सिग्नल")

ticker = st.text_input("स्टॉक का नाम लिखें (जैसे: SBIN.NS):", "RELIANCE.NS")
data = yf.download(ticker, period="3mo", interval="1d")

if not data.empty:
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Market")])

    for i in range(1, len(data)):
        if data['Close'].iloc[i] > data['SMA20'].iloc[i] and data['Close'].iloc[i-1] <= data['SMA20'].iloc[i-1]:
            fig.add_annotation(x=data.index[i], y=data['Low'].iloc[i], text="🚀 BUY", showarrow=True, arrowhead=1, arrowcolor="green", color="green")
        elif data['Close'].iloc[i] < data['SMA20'].iloc[i] and data['Close'].iloc[i-1] >= data['SMA20'].iloc[i-1]:
            fig.add_annotation(x=data.index[i], y=data['High'].iloc[i], text="🔻 SELL", showarrow=True, arrowhead=1, arrowcolor="red", color="red")

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    st.success("चार्ट पर 'BUY' और 'SELL' के निशान देखें।")
else:
    st.error("डेटा नहीं मिला।")

