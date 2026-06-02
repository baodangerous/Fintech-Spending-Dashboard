import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Fintech Spending Dashboard",
    page_icon="💳",
    layout="wide"
)

st.markdown("<h1 style='text-align: center; margin-bottom: 0.25em;'>FINTECH SPENDING DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; margin-top: 0;'>Phân tích hành vi chi tiêu và phát hiện giao dịch bất thường</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    local_file = "data/PS_20174392719_1491204439457_log.csv"
    cloud_file = "data/sample.csv"
    if os.path.exists(local_file):
        df = pd.read_csv(local_file, nrows=50000)
    else:
        df = pd.read_csv(cloud_file)
    return df

with st.spinner("Đang tải dữ liệu..."):
    df = load_data()

st.sidebar.header("Bộ lọc")
all_types = df["type"].unique().tolist()
selected_types = st.sidebar.multiselect(
    "Loại giao dịch",
    options=all_types,
    default=all_types
)
fraud_filter = st.sidebar.radio(
    "Trạng thái giao dịch",
    options=["Tất cả", "Bình thường", "Fraud"]
)
df = df[df["type"].isin(selected_types)]
if fraud_filter == "Fraud":
    df = df[df["isFraud"] == 1]
elif fraud_filter == "Bình thường":
    df = df[df["isFraud"] == 0]

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

st.markdown("---")
st.subheader("Phát hiện giao dịch bất thường")

def detect_anomaly(row):
    reasons = []
    if row["newbalanceOrig"] == 0 and row["oldbalanceOrg"] > 0:
        reasons.append("Số dư về 0")
    if row["amount"] > df["amount"].quantile(0.99):
        reasons.append("Số tiền bất thường lớn")
    if row["type"] in ["TRANSFER", "CASH_OUT"] and row["amount"] > 200000:
        reasons.append("Chuyển/rút tiền lớn")
    return ", ".join(reasons) if reasons else "Bình thường"

df["anomaly_reason"] = df.apply(detect_anomaly, axis=1)
anomaly_df = df[df["anomaly_reason"] != "Bình thường"]

col1, col2 = st.columns(2)
with col1:
    st.metric("Giao dịch bất thường phát hiện", f"{len(anomaly_df):,}")
with col2:
    st.metric("Tỷ lệ bất thường", f"{len(anomaly_df)/len(df)*100:.1f}%")
st.dataframe(anomaly_df[["type", "amount", "oldbalanceOrg",
                          "newbalanceOrig", "isFraud",
                          "anomaly_reason"]].head(20))

st.markdown("---")
st.subheader("Phân tích giao dịch theo thời gian")
step_data = df.groupby("step").agg(
    total=("amount", "sum"),
    count=("amount", "count"),
    fraud=("isFraud", "sum")
).reset_index()

col1, col2 = st.columns(2)
with col1:
    fig4 = px.line(step_data, x="step", y="count",
                   title="Số lượng giao dịch theo giờ",
                   labels={"step": "Giờ", "count": "Số giao dịch"})
    st.plotly_chart(fig4, use_container_width=True)
with col2:
    fig5 = px.line(step_data, x="step", y="fraud",
                   title="Giao dịch Fraud theo giờ",
                   labels={"step": "Giờ", "fraud": "Số fraud"},
                   color_discrete_sequence=["red"])
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("Top 10 tài khoản rủi ro cao nhất")
top_risk = df[df["isFraud"] == 1].groupby("nameOrig").agg(
    so_lan_fraud=("isFraud", "count"),
    tong_tien=("amount", "sum")
).reset_index().sort_values("so_lan_fraud", ascending=False).head(10)
top_risk.columns = ["Tài khoản", "Số lần Fraud", "Tổng tiền"]
top_risk["Tổng tiền"] = top_risk["Tổng tiền"].apply(lambda x: f"{x:,.0f}")
st.dataframe(top_risk.reset_index(drop=True), use_container_width=True)