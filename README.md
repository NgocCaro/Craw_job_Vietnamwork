# VietnamWorks Job Scraper & Data Cleaning

## 📌 Giới thiệu
Dự án này thực hiện **crawl dữ liệu tuyển dụng từ VietnamWorks** (ví dụ: Data Analyst tại Hà Nội) bằng Selenium + BeautifulSoup.  
Sau khi crawl, dữ liệu được **làm sạch (data cleaning)** và xuất ra file Excel để sử dụng trong phân tích / trực quan hóa bằng Power BI.

## 🛠️ Công nghệ sử dụng
- Python 3.x
- Selenium + WebDriver Manager
- BeautifulSoup4
- Pandas
- OpenPyXL
- Power BI (dashboard phân tích)

## 🚀 Tính năng
1. **Crawl dữ liệu VietnamWorks**
   - Tiêu đề công việc
   - Công ty
   - Mức lương
   - Kinh nghiệm yêu cầu
   - Kỹ năng
   - Ngành nghề, lĩnh vực
   - Hạn nộp hồ sơ (deadline)

2. **Data Cleaning**
   - Chuẩn hóa hạn nộp (chuyển "Hết hạn trong 13 ngày" → thành ngày cụ thể `YYYY-MM-DD`).
   - Chuẩn hóa lương (lọc bỏ “Thương lượng”, quy đổi về VND, tách thành min_salary, max_salary, avg_salary).
   - Chuẩn hóa kinh nghiệm (chuyển dạng text thành số năm kinh nghiệm).
   - Xuất file `jobs_vnw_clean.xlsx`.

3. **Phân tích dữ liệu (Power BI)**
   - **Salary Insights**: phân phối lương, so sánh ngành nghề, tìm công ty trả lương cao.
   - **Job Market Trends**: top kỹ năng, xu hướng deadline tuyển dụng.
   - **Company & Location Analysis**: bản đồ địa điểm, so sánh số lượng việc theo công ty.

## 📂 Cấu trúc thư mục
📁 Craw_job_vietnamwork
┣ 📜 vietnamwork.py # Script crawl dữ liệu
┣ 📜 clean_data.py # Script làm sạch dữ liệu
┣ 📜 jobs_vnw_full.xlsx # Dữ liệu gốc (crawl)
┣ 📜 jobs_vnw_clean.xlsx # Dữ liệu đã làm sạch
┣ 📜 README.md # Mô tả dự án
