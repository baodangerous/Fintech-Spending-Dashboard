import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fintech Spending Dashboard",
    page_icon="💳",
    layout="wide"
)

st.markdown("<h1 style='text-align: center; margin-bottom: 0.25em;'>FINTECH SPENDING DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; margin-top: 0;'>Phân tích hành vi chi tiêu và phát hiện giao dịch bất thường</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/sample.csv")
    return df

with st.spinner("Đang tải dữ liệu..."):
    df = load_data()

st.success(f"Đã tải {len(df):,} giao dịch")
st.dataframe(df.head(10))

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Tổng giao dịch", f"{len(df):,}")
with col2:
    st.metric("Tổng giá trị", f"{df['amount'].sum()/1e9:.1f}B")
with col3:
    fraud_total = df["isFraud"].sum()
    st.metric("Giao dịch Fraud", f"{fraud_total:,}")
with col4:
    fraud_rate = df["isFraud"].mean() * 100
    st.metric("Tỷ lệ Fraud", f"{fraud_rate:.2f}%")

st.markdown("---")
st.subheader("Phân tích theo loại giao dịch")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(df, names="type", title="Tỷ lệ loại giao dịch")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    type_amount = df.groupby("type")["amount"].sum().reset_index()
    fig2 = px.bar(type_amount, x="type", y="amount", title="Tổng tiền theo loại giao dịch")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("Thống kê Fraud")

fraud_count = df["isFraud"].value_counts().reset_index()
fraud_count.columns = ["isFraud", "count"]
fraud_count["label"] = fraud_count["isFraud"].map({0: "Bình thường", 1: "Fraud"})

fig3 = px.pie(fraud_count, names="label", values="count",
              title="Tỷ lệ giao dịch Fraud vs Bình thường",
              color_discrete_map={"Fraud": "red", "Bình thường": "green"})
st.plotly_chart(fig3, use_container_width=True)