import time
import csv
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DataCollector:
    def __init__(self, url, css_selector_name, css_selector_price, db_name):
        self.url = url
        self.css_selector_name = css_selector_name
        self.css_selector_price = css_selector_price
        self.db_name = db_name

    def collect_data(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(self.url)
        time.sleep(5)

        data = []
        items = driver.find_elements(By.CSS_SELECTOR, '.product-info')
        for item in items:
            try:
                name = item.find_element(By.CSS_SELECTOR, self.css_selector_name).text.strip()
                price = item.find_element(By.CSS_SELECTOR, self.css_selector_price).text.strip()
                data.append((name, price))
                print(f"{name} : {price}")
            except Exception as e:
                print("Error collecting data:", e)

        driver.quit()
        return data

    def save_to_csv(self, data, filename):
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Product Name", "Price"])
            writer.writerows(data)
        print(f"Data saved to {filename}")

    def save_to_db(self, data, table_name):
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=tcp:your_server.database.windows.net,1433;"
            f"Database={self.db_name};"
            "Uid=your_username;"
            "Pwd=your_password;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ProductName NVARCHAR(255), Price NVARCHAR(50))")
        for item in data:
            cursor.execute(f"INSERT INTO {table_name} (ProductName, Price) VALUES (?, ?)", item)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Data inserted into {table_name} in {self.db_name} database.")


# Example usage
collector = DataCollector(
    url="https://cellphones.com.vn/laptop.html",
    css_selector_name=".product__name",
    css_selector_price=".product__price--show",
    db_name="ProductDB"
)

# Collect data and save
data = collector.collect_data()
collector.save_to_csv(data, "product_data.csv")
collector.save_to_db(data, "LaptopData")
