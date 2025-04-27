import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

url = 'https://www.vnexpress.net/'
headers = {
    'User-Agent': "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

new_feeds = soup.findAll(class_="item-news")

# Tạo tên file CSV với timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"vnexpress_crawl.csv"

# Mở file CSV để ghi dữ liệu
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    # Định nghĩa các trường
    fieldnames = ['stt', 'title', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Ghi header
    writer.writeheader()
    
    # Ghi dữ liệu
    stt = 1
    for nfeed in new_feeds:
        feed = nfeed.find("a")
        if feed is None:
            continue
        title = feed.get("title")
        link = feed.get("href")
        if not title or not link:
            continue
        
        # In ra màn hình với định dạng mới
        print(f"--------- Bài viết {stt} ---------")
        print(f"Tiêu đề: {title}")
        print(f"Đường dẫn: {link}")
        print()
        
        # Ghi vào CSV
        writer.writerow({
            'stt': stt,
            'title': title, 
            'link': link
        })
        
        stt += 1

print(f"Đã xuất dữ liệu vào file: {csv_filename}")