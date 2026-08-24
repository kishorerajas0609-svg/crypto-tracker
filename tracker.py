import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

headless_mode = True
options = webdriver.ChromeOptions()
if headless_mode:
    options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://coinmarketcap.com/")
time.sleep(5)
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
data = []
timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 5 and cells[1].text.strip().isdigit():
        change = cells[5].text.strip()
        if "icon-Caret-down" in cells[5].get_attribute("innerHTML"):
            change = "-" + change
        data.append({
            "Timestamp": timestamp,
            "Name": cells[2].text.split("\n")[0],
            "Price": cells[3].text.strip(),
            "Change_24H": change,
            "Market_Cap": cells[7].text.split("\n")[0]
        })
        if len(data) == 10:
            break
driver.quit()
df = pd.DataFrame(data)
print("\nTop 10 Cryptocurrencies:\n", df)
csv_file = "crypto_prices.csv"
try:
    df.to_csv(csv_file, mode="x", index=False)
except FileExistsError:
    df.to_csv(csv_file, mode="a", header=False, index=False)

