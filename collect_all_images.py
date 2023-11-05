import time
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import requests
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def clean_filename(fname):
    fname = re.sub(r'[\/:*?"<>|]', '_', fname)
    fname = fname.replace('//', '/')
    return fname


def clean_extension(filename):
    known_extensions = ['.svg', '.jpg', '.png', '.webp']

    for ext in known_extensions:
        if ext in filename:
            return filename.split(ext, 1)[0] + ext

    return filename


def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options)
    return driver


def scrape_site(url, save_folder, headers):
    driver = get_webdriver()
    driver.get(url)

    os.makedirs(save_folder, exist_ok=True)

    scroll_count = 0
    downloaded_urls = set()
    image_counter = 1

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        element_locator = driver.find_element(By.CSS_SELECTOR, 'body')
        ActionChains(driver).move_to_element(element_locator).perform()

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        pic_tags = soup.find_all("picture")

        for pic in pic_tags:
            img_tag = pic.find('img')
            img_sources = []

            img_src = img_tag.get('src')
            if img_src:
                img_sources.append(img_src)

            for image_url in img_sources:

                if image_url in downloaded_urls:
                    continue

                if image_url.startswith('data'):
                    continue

                if '.mp4' in image_url:
                    continue

                try:
                    if image_url.startswith('https'):
                        image_data = requests.get(image_url, headers).content
                    else:
                        image_data = requests.get(url + image_url, headers).content

                    try:
                        image_filename = os.path.basename(image_url)
                        image_filename = clean_filename(image_filename)
                    except Exception as e:
                        image_filename = ""
                        print(e)

                    filename = os.path.join(save_folder, f'{image_counter}-{image_filename}')
                    filename = clean_extension(filename)

                    try:
                        with open(filename, 'wb') as f:
                            f.write(image_data)

                        print("Downloaded:", filename)

                        if 'homepage-logos' in filename:
                            val = img_tag.get('class')
                            string_val = ""
                            if len(val) > 1:
                                for v in val[:-1]:
                                    string_val += v + " "
                            else:
                                for v in val:
                                    string_val += v + " "
                            try:
                                # print(string_val)
                                print(soup.find('img', class_=string_val))
                            except Exception as e:
                                print(e)

                        downloaded_urls.add(image_url)
                        image_counter += 1
                    except Exception as e:
                        print(f"Error while saving the image: {e}")

                except Exception as e:
                    print(e)

        scroll_count += 1

        if scroll_count >= 10:
            break

    driver.quit()


if __name__ == "__main__":
    base_url = 'https://fylehq.com'
    folder = 'images\\temp'
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    scrape_site(base_url, folder, custom_headers)
