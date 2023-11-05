import os
import re
import time
import uuid
from flashtext import KeywordProcessor
from bs4 import BeautifulSoup
from selenium import webdriver


def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options)
    return driver


# flashtext implementation
def get_rel_text(url):
    driver = get_webdriver()
    driver.get(url)

    words = ["companies", "partners", "trusted", "operators", "firms", "businesses", "enterprises", "corporations"]

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    soup_text = soup.get_text()

    keyword_processor = KeywordProcessor()

    keyword_processor.add_keywords_from_list(words)
    text_to_find = keyword_processor.extract_keywords(soup_text)

    print(text_to_find)

    return


def download_image(image_url, save_folder, image_data):
    # Download image
    os.makedirs(save_folder, exist_ok=True)

    img_extension = image_url.split('.')[-1]
    img_filename = os.path.join(f'{save_folder}', f'{uuid.uuid4()}_image.{img_extension}')
    with open(img_filename, 'wb') as img_file:
        img_file.write(image_data)
    print(f'Downloaded and saved the image to {img_filename}')


def relevant_imgs(img_tags, im_urls, url):
    for img in img_tags:
        img_src = img['src']

        if img_src:
            if img_src.startswith('data') or '.mp4' in img_src:
                continue

            if img_src.startswith('https'):
                # image_data = requests.get(img_src).content
                im_urls.add(img_src)
                # download_image(img_src, 'temp_folder', image_data)
            else:
                # image_data = requests.get(url + img_src).content
                im_urls.add(url+img_src)
                # download_image(url + img_src, 'temp_folder', image_data)


def text_plus_links(url):
    driver = get_webdriver()
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    words = ["companies", "partners", "operators", "businesses", "clients", "Our customers", "logos"]

    div_tags = soup.find_all('div')

    rel_text = ""
    im_urls = set()
    img_tags = []

    for div in div_tags:
        div_text = div.get_text().lower()
        pattern = r'([A-Za-z])(\d)'
        result = re.sub(pattern, r'\1 \2', div_text)

        # "logos" filter
        # if div.has_attr('class'):
        #     div_class = " ".join(div['class'].split('_'))
        #     if "logos" in div_class.lower():
        #         print(div_class)

        for word in words:
            if word in result:
                rel_text = div_text
                img_tags = div.findAll('img')  # list of img tags

    relevant_imgs(img_tags, im_urls, url)

    print(rel_text + str([i for i in im_urls]))

    return im_urls


if __name__ == '__main__':
    start = time.time()
    # get_rel_text('https://www.pazcare.com/')
    text_plus_links('https://www.pazcare.com/')
    end = time.time()
    print(str(end - start) + " seconds")
