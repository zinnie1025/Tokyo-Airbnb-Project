from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
import re
import time

# TODO : 도쿄 지하철(도쿄 메트로) 수집


def load_page(url):
    driver = ChromeDriverManager().install()
    service = Service(excutable_path=driver)
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    # browser.fullscreen_window()

    return browser


def get_content(browser):
    """
    도쿄 지하철 역 라인별 수집
    """
    main_train = list()
    metro_link = {}
    # href 링크 가져오기
    metro_child = browser.find_elements(
        By.CSS_SELECTOR, "#v2_about > div.v2_wrapper > a"
    )

    for metro in metro_child:
        station = metro.find_element(By.CSS_SELECTOR, "p").text
        main_train.append(station)
        metro_link[station] = metro.get_attribute("href")
    line_detail = get_line_detail(browser, metro_link)

    return line_detail


def get_line_detail(browser, metro_link):
    line_detail_dict = {}

    for metro, link in metro_link.items():
        line_list = list()

        browser.get(link)
        time.sleep(3)

        line_detail = browser.find_elements(
            By.CSS_SELECTOR, "td.v2_cellStation > p > span > a"
        )

        for line in line_detail:
            line_list.append(line.text)

        line_detail_dict[metro] = line_list

    return line_detail_dict


url = "https://www.tokyometro.jp/en/subwaymap/index.html"
browser = load_page(url)
line_detail = get_content(browser)
line_detail