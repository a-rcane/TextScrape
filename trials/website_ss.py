import os
import time
from urllib.parse import urlparse

import cv2
import keras_ocr
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def fullpage_screenshot(url, save_folder, image_name):
    os.makedirs(save_folder, exist_ok=True)

    driver = get_webdriver()
    driver.get(url)
    time.sleep(2)

    element_locator = driver.find_element(By.CSS_SELECTOR, 'body')
    ActionChains(driver).move_to_element(element_locator).perform()

    # height size 33%
    height = driver.execute_script("return document.body.scrollHeight")/3
    driver.set_window_size(1000, height)

    filename = save_folder + f"/{image_name}"
    driver.save_screenshot(filename)
    print(f"Downloaded: {filename}")
    driver.quit()


def generate_image_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    parts = domain.split('.')
    if len(parts) > 1:
        domain = parts[0]

    domain += ".png"

    return domain


def get_text_from_img():
    pipeline = keras_ocr.pipeline.Pipeline()
    image = cv2.imread('Temp/25-homepage-logos.png')

    images = [image]
    prediction_groups = pipeline.recognize(images)

    print(f"{prediction_groups}")

    return prediction_groups


if __name__ == "__main__":
    # base_url = ["https://snackpass.co", "https://fylehq.com", "https://plumhq.com", "https://yokoy.io/"]
    # folder = "Temp"
    # for u in base_url:
    #     img_name = generate_image_name(u)
    #     fullpage_screenshot(u, folder, img_name)
    get_text_from_img()
