import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ---------- Setup Selenium ----------
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL gốc (đổi từ khóa, địa điểm ở đây)
url = "https://www.vietnamworks.com/viec-lam?q=data%20analyst&l=24&g=5"

job_list = []
page = 1

# ---------- Crawl danh sách ----------
while True:
    print(f"📄 Crawl trang {page} ...")
    driver.get(url + f"&page={page}")
    time.sleep(4)

    # Scroll xuống cuối để load hết job
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    jobs = driver.find_elements(By.CSS_SELECTOR, "div.search_list.view_job_item")
    if not jobs:
        print("🚩 Hết trang rồi.")
        break

    for job in jobs:
        title, link, company, salary = None, None, None, None

        try:
            title_elem = job.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_elem.text.strip()
            link = title_elem.get_attribute("href")
        except:
            pass

        try:
            company_elem = job.find_element(By.CSS_SELECTOR, "a[href*='/nha-tuyen-dung/']")
            company = company_elem.text.strip()
        except:
            pass

        try:
            salary_elem = job.find_element(By.CSS_SELECTOR, "span.sc-fgSWkL")
            salary = salary_elem.text.strip()
        except:
            pass

        # Nếu có link thì đi sâu bằng requests
        experience, skills, deadline, location, industry, field = None, None, None, None, None, None
        if link:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(link, headers=headers, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")

                    # Số năm kinh nghiệm
                    exp_elem = soup.find("label", string=lambda x: x and "SỐ NĂM KINH NGHIỆM" in x)
                    if exp_elem:
                        p = exp_elem.find_next("p")
                        experience = p.get_text(strip=True) if p else None

                    # Kỹ năng
                    skills_elem = soup.find("label", string=lambda x: x and "KỸ NĂNG" in x)
                    if skills_elem:
                        p = skills_elem.find_next("p")
                        skills = p.get_text(strip=True) if p else None

                    # Deadline
                    deadline_elem = soup.find("span", string=lambda x: x and "Hết hạn trong" in x)
                    if deadline_elem:
                        deadline = deadline_elem.get_text(strip=True)

                    # Địa điểm làm việc
                    location_elem = soup.find("h2", string="Địa điểm làm việc")
                    if location_elem:
                        p = location_elem.find_next("p")
                        location = p.get_text(strip=True) if p else None

                    # Ngành nghề
                    industry_label = soup.find("label", string="NGÀNH NGHỀ")
                    if industry_label:
                        p = industry_label.find_next("p")
                        industry = p.get_text(" > ", strip=True) if p else None

                    # Lĩnh vực
                    field_label = soup.find("label", string="LĨNH VỰC")
                    if field_label:
                        p = field_label.find_next("p")
                        field = p.get_text(strip=True) if p else None

                    

            except Exception as e:
                print("❌ Lỗi crawl detail:", e)

        if title:
            job_list.append({
                "title": title,
                "company": company,
                "salary": salary,
                "link": link,
                "experience": experience,
                "skills": skills,
                "deadline": deadline,
                "location": location,
                "industry": industry,
                "field": field
                
            })

    print(f"✅ Trang {page}: {len(jobs)} job, tổng cộng {len(job_list)} job")
    page += 1

# ---------- Xuất Excel ----------
df = pd.DataFrame(job_list)
df.to_excel("jobs_vnw_full.xlsx", index=False, engine="openpyxl")

driver.quit()
print(f"🎉 Crawl xong {len(df)} job, dữ liệu đã lưu vào jobs_vnw_full.xlsx")
