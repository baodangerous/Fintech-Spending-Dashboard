# BA Document — Fintech Spending Dashboard

**Người thực hiện:** Nguyen Le Bao Dang  
**Ngày:** 02/06/2026  
**Version:** 1.0

---

## 1. Bối cảnh & Bài toán

### Bối cảnh
Thị trường ví điện tử Việt Nam đang tăng trưởng mạnh với hơn 40 ví được cấp phép.
MoMo, ZaloPay, VNPay xử lý hàng triệu giao dịch mỗi ngày.
Fraud và giao dịch bất thường là thách thức lớn nhất — gây thiệt hại tài chính
và mất niềm tin của người dùng.

### Bài toán
> Làm thế nào để phát hiện sớm giao dịch bất thường trong hệ thống ví điện tử
> nhằm giảm thiểu rủi ro fraud và bảo vệ người dùng?

---

## 2. Stakeholder

| Stakeholder | Vai trò | Quan tâm đến |
|-------------|---------|--------------|
| Risk & Fraud team | Xử lý giao dịch bất thường | Độ chính xác detection, false positive rate |
| Product team | Ra quyết định tính năng | User experience, không làm khó user bình thường |
| Data team | Cung cấp và phân tích data | Data quality, pipeline ổn định |
| Ban lãnh đạo | Quyết định đầu tư | Thiệt hại tài chính, tỷ lệ fraud tổng thể |

---

## 3. Yêu cầu

### Business Requirements
- Phát hiện được giao dịch có dấu hiệu bất thường theo business rule
- Phân loại được lý do bất thường cụ thể
- Dashboard trực quan để team fraud theo dõi hàng ngày

### Functional Requirements
- Lọc giao dịch theo loại (PAYMENT, TRANSFER, CASH_OUT...)
- Lọc theo trạng thái (Tất cả / Bình thường / Fraud)
- Hiển thị metric tổng quan: tổng giao dịch, tổng tiền, tỷ lệ fraud
- Phát hiện anomaly theo rule-based
- Hiển thị lý do bất thường từng giao dịch

### Non-functional Requirements
- Load data dưới 3 giây
- Giao diện đơn giản, không cần training để dùng

---

## 4. Business Rules — Anomaly Detection

| Rule | Điều kiện | Lý do |
|------|-----------|-------|
| Rule 1 | Số dư về 0 sau giao dịch | Dấu hiệu rút hết tiền — thường gặp trong fraud |
| Rule 2 | Số tiền thuộc top 1% | Giao dịch bất thường lớn so với toàn hệ thống |
| Rule 3 | TRANSFER/CASH_OUT > 200,000 | Chuyển/rút tiền lớn cần kiểm tra thêm |

---

## 5. Key Insights từ Data

- **15.5% giao dịch** có dấu hiệu bất thường theo rule-based
- **TRANSFER và CASH_OUT** chiếm tỷ lệ tiền lớn nhất — rủi ro cao nhất
- **Tỷ lệ Fraud thật: 0.20%** — hệ thống rule-based đang over-detect
- **100% fraud tập trung ở TRANSFER và CASH_OUT** — có thể dùng để filter

---

## 6. Đề xuất hành động

| Insight | Đề xuất |
|---------|---------|
| Rule 1 phát hiện nhiều false positive | Kết hợp thêm điều kiện: số dư về 0 + số tiền lớn |
| TRANSFER/CASH_OUT rủi ro cao | Thêm bước xác thực OTP cho giao dịch > 5 triệu |
| Tỷ lệ fraud thật 0.20% | Cần ML model để giảm false positive rate |

---

## 7. Hướng phát triển tiếp theo

- Áp dụng ML model (Isolation Forest) để phát hiện anomaly chính xác hơn
- Thêm time-series analysis: phát hiện giao dịch bất thường theo giờ
- Tích hợp alert system: tự động gửi thông báo khi phát hiện fraud