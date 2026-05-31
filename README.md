# FINTECH SPENDING DASHBOARD

Phân tích hành vi chi tiêu và phát hiện giao dịch bất thường trong hệ thống ví điện tử.

## Bài toán
Fraud detection là một trong những thách thức lớn nhất của Fintech. 
Project này phân tích 50,000 giao dịch từ dataset PaySim để:
- Hiểu pattern chi tiêu theo loại giao dịch
- Phát hiện giao dịch bất thường
- Trực quan hoá dữ liệu qua dashboard tương tác

## Tech Stack
- Python + Pandas
- Plotly
- Streamlit

## Dataset
Download từ Kaggle: https://www.kaggle.com/datasets/ealaxi/paysim1  
Sau khi tải, đặt file CSV vào thư mục `data/`

## Chạy app
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Key Insights
- TRANSFER và CASH_OUT chiếm tỷ lệ tiền lớn nhất
- Tỷ lệ Fraud: 0.20% — dữ liệu imbalanced như thực tế
- 100% giao dịch Fraud tập trung ở TRANSFER và CASH_OUT