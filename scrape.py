import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from concurrent.futures import ThreadPoolExecutor

output_folder = os.path.join(os.getcwd(), "product_images")
os.makedirs(output_folder, exist_ok=True)

# Set up Selenium with Firefox
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.set_preference("permissions.default.image", 2)  # Block images
    # options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", False)  # Disable Flash plugins
    driver_path = "/opt/homebrew/bin/geckodriver"
    service = Service(driver_path)
    return webdriver.Firefox(service=service, options=options)

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")

def extract_page_number(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    page_number = query_params.get('page', [1])[0]
    return int(page_number)

def update_url_with_page(url, page_number):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['page'] = [str(page_number)]
    updated_query = urlencode(query_params, doseq=True)
    updated_url = urlunparse(parsed_url._replace(query=updated_query))
    return updated_url

# Main function
def scrape_digikala(base_url):
    driver = setup_driver()
    start_page = extract_page_number(base_url)
    current_page = start_page

    driver.get(base_url)

    while True:
        print(f"Processing page {current_page}...")
        try:
            product_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, "//*[@id='ProductListPagesWrapper']//section[1]/div[2]"
                ))
            )
            product_divs = product_container.find_elements(By.XPATH, './/div[@data-product-index]')
            print(f"Found {len(product_divs)} products")
            if not product_divs:
                print(f"No products found on page {current_page}. Terminating.")
                break
        except Exception as e:
            print(f"Failed to locate product container or child divs on page {current_page}: {e}")
            break

        product_links = []
        for product_div in product_divs:
            try:
                anchor = product_div.find_element(By.TAG_NAME, 'a')
                product_links.append(anchor.get_attribute('href'))
            except:
                continue

        for i, product_link in enumerate(product_links):
            print(f"Opening product {i + 1} on page {current_page}: {product_link}")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(product_link)

            try:
                image_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-main-image-src]"))
                )
                first_div = image_element.find_element(By.XPATH, "./div[1]")
                second_div = first_div.find_element(By.XPATH, "./div[2]")
                target_div = second_div.find_element(By.XPATH, "./div[1]")

                driver.execute_script("arguments[0].click();", target_div)

                image_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//*[@id="modal-root"]/div/div/div/div/div/div/div[1]/div[3]/div/div/div/div/div/div[1]/div'))
                )
                images = image_container.find_elements(By.XPATH, './/div/div/picture/img')

                for idx, img in enumerate(images):
                    img_src = img.get_attribute('src')
                    save_path = os.path.join(output_folder, f"product_page_{current_page}_item_{i + 1}_img_{idx + 1}.jpg")
                    download_image(img_src, save_path)

            except Exception as e:
                print(f"Failed to process product {product_link}: {e}")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        current_page += 1
        next_page_url = update_url_with_page(base_url, current_page)
        try:
            driver.get(next_page_url)
            time.sleep(3)
        except Exception as e:
            print(f"Failed to load page {current_page}: {e}")
            break

    driver.quit()
    print("Scraping completed.")

# Input URL
if __name__ == "__main__":
    base_url = input("Enter the URL (e.g., https://www.digikala.com/search/category-notebook-netbook-ultrabook/asus/?page=1): \n")
    scrape_digikala(base_url)