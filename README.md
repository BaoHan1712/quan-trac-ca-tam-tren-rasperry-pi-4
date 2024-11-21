# 🎣 Ứng Dụng Quang Trắc Cá Tầm

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=40&pause=1000&color=F7AA36&center=true&vCenter=true&width=600&lines=H%E1%BB%87+Th%E1%BB%91ng+Quang+Tr%E1%BA%AFc+C%C3%A1+%F0%9F%90%9F" alt="Typing SVG" />
</div>

## 📋 Mục Lục
- [Tổng Quan](#-tổng-quan)
- [Tính Năng Chính](#-tính-năng-chính)
- [Cấu Trúc Hệ Thống](#-cấu-trúc-hệ-thống)
- [Cài Đặt](#-cài-đặt)
- [Giao Diện](#-giao-diện)

## 🌟 Tổng Quan
Hệ thống giám sát chất lượng nước trong bể cá tầm, sử dụng các cảm biến để theo dõi và cảnh báo khi có bất thường.

## 🚀 Tính Năng Chính

### 📊 Giám Sát Thời Gian Thực
- Theo dõi dữ liệu từ 2 cảm biến độc lập
- Hiển thị giá trị đo được theo thời gian thực
- Tính toán giá trị trung bình mỗi 10 lần đo

### ⚠️ Hệ Thống Cảnh Báo
- 🔔 Chuông báo khi phát hiện nước đục
- 💡 Đèn LED cảnh báo khi:
  - Pin cảm biến yếu (<15%)
  - Cảm biến mất kết nối
  - Phát hiện nước đục

### 🔄 Xử Lý Dữ Liệu
- Lưu trữ dữ liệu vào Excel theo ngày
- Tự động tính toán giá trị đột biến
- Phát hiện và xử lý mất kết nối

### 🛠️ Quản Lý Thiết Bị
- Cài đặt ngưỡng cảnh báo cho từng cảm biến
- Điều khiển thời gian vệ sinh cảm biến
- Giám sát pin của các cảm biến

### 🌐 Kết Nối
- Giao tiếp UART với các cảm biến
- Kết nối WebSocket với server
- Tự động kết nối lại khi mất kết nối

## 🔧 Cấu Trúc Hệ Thống

```mermaid
graph TD
    A[Cảm Biến 1] -->|UART| C[Raspberry Pi]
    B[Cảm Biến 2] -->|UART| C
    C -->|WebSocket| D[Server]
    C -->|Điều Khiển| E[Chuông Báo]
    C -->|Điều Khiển| F[Đèn LED]
    C -->|Lưu Trữ| G[Excel]

```

## 💻 Giao Diện
- Hiển thị trạng thái cảm biến
- Biểu đồ theo dõi dữ liệu
- Bảng điều khiển cài đặt
- Nút xuất dữ liệu Excel

<div align="center">
  <img src="assets/header.png" alt="Header" width="800"/>
</div>

## 🔌 Cài Đặt
1. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

2. Kết nối thiết bị qua cổng USB

3. Chạy chương trình:
```bash
python main.py
```

## 📝 Ghi Chú
- Đường dẫn lưu file: `/home/ailab/Downloads/luu_ca_tam`
- Cổng kết nối mặc định: `/dev/ttyUSB0`


---
<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white"/>
</div>
