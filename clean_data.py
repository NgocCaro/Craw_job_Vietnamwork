import pandas as pd
from datetime import datetime, timedelta
import re

# Đọc file Excel đã crawl
df = pd.read_excel("jobs_vnw_full.xlsx")

# =========================
# 1. Clean deadline
# =========================
def clean_deadline(deadline_text):
    if pd.isna(deadline_text):
        return None
    text = str(deadline_text)
    
    # Trường hợp "Hết hạn trong 10 giờ"
    if "giờ" in text:
        return (datetime.today() + timedelta(days=0)).strftime("%Y-%m-%d")
    
    # Trường hợp "Hết hạn trong X ngày"
    match = re.search(r"(\d+)", text)
    if match:
        days_left = int(match.group(1))
        return (datetime.today() + timedelta(days=days_left)).strftime("%Y-%m-%d")
    
    return None

df["deadline_clean"] = df["deadline"].apply(clean_deadline)

# =========================
# 2. Clean salary
# =========================
usd_to_vnd = 25000  # tỷ giá USD → VND

def parse_salary(salary_text):
    if not isinstance(salary_text, str) or "thương lượng" in salary_text.lower():
        return None, None, None

    text = salary_text.replace(",", "").lower()

    # --- 2.1 VND ---
    if "tr" in text or "₫" in text:
        nums = [float(x) for x in re.findall(r"\d+", text)]
        nums = [n * 1_000_000 for n in nums]  # triệu → VND

        if "năm" in text:  # đổi năm → tháng
            nums = [n/12 for n in nums]

        if len(nums) == 1:
            return nums[0], nums[0], nums[0]
        elif len(nums) >= 2:
            return min(nums), max(nums), sum(nums)/len(nums)

    # --- 2.2 USD ---
    if "$" in text:
        nums = [float(x) for x in re.findall(r"\d+", text)]
        nums = [n * usd_to_vnd for n in nums]

        if "năm" in text:  # đổi năm → tháng
            nums = [n/12 for n in nums]

        if len(nums) == 1:
            return nums[0], nums[0], nums[0]
        elif len(nums) >= 2:
            return min(nums), max(nums), sum(nums)/len(nums)

    return None, None, None

# Áp dụng vào DataFrame
df[["min_salary", "max_salary", "avg_salary"]] = df["salary"].apply(
    lambda x: pd.Series(parse_salary(x))
)
# =========================
# 3. Clean experience (1 cột)
# =========================
def clean_experience(exp_text):
    if not isinstance(exp_text, str):
        return None
    text = exp_text.lower()

    if "không yêu cầu" in text:
        return 0

    nums = [int(x) for x in re.findall(r"\d+", text)]
    if nums:
        return min(nums)  # lấy số nhỏ nhất (ví dụ "3-5 năm" thì lấy 3)
    
    return None

df["experience_clean"] = df["experience"].apply(clean_experience)
# =========================

# =========================
# 4. Xóa cột gốc
# =========================
df = df.drop(columns=["experience", "salary", "deadline"])

# 3. Xuất file
# =========================
df.to_excel("jobs_vnw_clean.xlsx", index=False, engine="openpyxl")
print("✅ Đã clean dữ liệu deadline & lương, lưu vào jobs_vnw_clean.xlsx")
