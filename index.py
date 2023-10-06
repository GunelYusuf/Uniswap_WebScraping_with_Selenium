import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


path = "../../Downloads/chromedriver-mac-x64/chromedriver"
driver = webdriver.Chrome(path)


website = 'https://v2.info.uniswap.org/pairs'
driver.get(website)

wait = WebDriverWait(driver, 20)

pair_xpath = "//div[@class='sc-hzDkRC kpsoyz']//div[@class='sc-Rmtcm kPxUfE css-1yh09yi']//div[@class='sc-bRBYWo ivEEsA']"
next_button_xpath = "//div[@class='sc-csuQGl krOsSz']/.."
next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))

page_count = 1
pair_names = []
pair_liquidity = []
pair_volume = []
pair_hash = []

while True:
    print(f"Page {page_count}")
    try:
        next_button.click()
    except:
        print("No more pages or an error occurred")
        break

    pairs = wait.until(EC.presence_of_all_elements_located((By.XPATH, pair_xpath)))
    for pair in pairs:
        name_element = pair.find_element_by_xpath(".//a[@class='sc-cSHVUG lnITpf']/div[@class='sc-jlyJG hZRHdD']")
        hash_element = pair.find_element_by_xpath(".//a[@class='sc-cSHVUG lnITpf']")
        liquidity_element = pair.find_element_by_xpath(".//div[@class='sc-VigVT dNgKCa']")
        volume_elements = pair.find_elements_by_xpath(".//div[@class='sc-VigVT dNgKCa']")
        if len(volume_elements) > 1:
            volume_element = volume_elements[1]
        else:
            volume_element = None

        name = name_element.text
        hashCode = hash_element.get_attribute("href")
        hash_ = hashCode.split("pair/")[1]
   
        liquidity = liquidity_element.text
        try:
          volume = volume_element.text if volume_element else "N/A"
        except StaleElementReferenceException:
          volume = "N/A"
        pair_names.append(name)
        pair_hash.append(hash_)
        pair_liquidity.append(liquidity)
        pair_volume.append(volume)


    a=driver.find_element(By.XPATH, '//div[@class = "sc-gipzik bMaYEG"]/div[@class = "sc-bdVaJa KpMoH css-1ecm0so"]').text[-1]
    current_page_number = int(a)
    print(current_page_number)
    time.sleep(2) 
    page_count += 1
    if current_page_number == page_count:
        print("Reached the last page")
        break
    previous_page_number = current_page_number
df= pd.DataFrame(list(zip(pair_names, pair_liquidity, pair_volume,pair_hash)), columns =['Pair Name', 'Liquidity', 'Volume', 'Hash_Code'])
df.to_csv('uniswap.csv', index=False)

driver.quit()