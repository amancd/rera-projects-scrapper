import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ——— Helper ———
def get_text_or_none(driver, by, locator, wait=None, timeout=5):
    try:
        if wait:
            return wait.until(EC.visibility_of_element_located((by, locator))).text.strip()
        return driver.find_element(by, locator).text.strip()
    except Exception:
        return None

# ——— Setup WebDriver ———
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get("https://rera.odisha.gov.in/projects/project-list")

# Wait for the cards to load
driver.get("https://rera.odisha.gov.in/projects/project-list")
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card.mb-3")))

results = []

for idx in range(6):
    # 1) re-find the actual cards
    cards = driver.find_elements(By.CSS_SELECTOR, "div.card.project-card.mb-3")
    if idx >= len(cards):
        print(f"Only {len(cards)} cards loaded — stopping at index {idx}.")
        break

    card = cards[idx]
    driver.execute_script("arguments[0].scrollIntoView(true);", card)
    time.sleep(0.5)

    # 2) click View Details
    card.find_element(By.XPATH, ".//a[contains(text(),'View Details')]").click()

    # 3) extract overview
    proj_name = get_text_or_none(
        driver, By.XPATH,
        "//label[contains(text(),'Project Name')]/following-sibling::strong",
        wait=wait
    )
    regd_no = get_text_or_none(
        driver, By.XPATH,
        "//label[contains(text(),'RERA Regd. No')]/following-sibling::strong"
    )

    # 4) extract promoter details
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Promoter Details']"))).click()
    time.sleep(1)

    # Try to extract Company Name
    comp_name = get_text_or_none(driver, By.XPATH, "//label[contains(text(),'Company Name')]/following-sibling::strong")

    # If not available, use Proprietor Name and Permanent Address
    if not comp_name:
        proprietor_name = get_text_or_none(driver, By.XPATH, "//label[contains(text(),'Propietory Name')]/following-sibling::strong")
        permanent_addr = get_text_or_none(driver, By.XPATH, "//label[contains(text(),'Permanent Address')]/following-sibling::strong")
        comp_name = proprietor_name if proprietor_name else "N/A"
        office_addr = permanent_addr if permanent_addr else "N/A"
    else:
        office_addr = get_text_or_none(driver, By.XPATH, "//label[contains(text(),'Registered Office Address')]/following-sibling::strong")

    # GST No (same logic for both)
    gst_no = get_text_or_none(driver, By.XPATH, "//label[contains(text(),'GST')]/following-sibling::strong")


    results.append({
            "Project Name": proj_name,
            "RERA Regd. No": regd_no,
            "Promoter Company Name": comp_name,
            "Promoter Registered Office Address": office_addr,
            "GST No": gst_no
        })

    try:
        driver.find_element(By.XPATH, "//button[contains(text(),'Close') or contains(text(),'Back')]").click()
    except:
        driver.back()

    # wait for the list to be present again before next iteration
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card.mb-3")))

# Save results
with open("rera_projects.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print("Saved", len(results), "records to rera_projects.json")
print(json.dumps(results, indent=2))

with open("rera_projects.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
    
driver.quit()