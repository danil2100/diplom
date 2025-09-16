import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-features=UseGpuRasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_select_departure_city(browser):
    browser.get("https://www.aviasales.ru/")
    browser.execute_script("""
        window.localStorage.setItem('city', 'IJK');
        window.localStorage.setItem('country', 'RU');
        window.localStorage.setItem('cityName', 'Ижевск');
    """)
    browser.refresh()
    field = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )
    value = field.get_attribute("value")
    assert "Ижевск" in value


def test_select_arrival_city(browser):
    browser.get("https://www.aviasales.ru/")
    browser.execute_script("""
        window.localStorage.setItem('city', 'IJK');
        window.localStorage.setItem('country', 'RU');
        window.localStorage.setItem('cityName', 'Ижевск');
    """)
    browser.refresh()
    field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Куда']"))
    )
    field.click()
    field.clear()
    field.send_keys("Москва")
    dropdown_option = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'SearchInput_suggestion') and contains(., 'Москва')]"))
    )
    dropdown_option.click()
    value = field.get_attribute("value")
    assert "Москва" in value


def test_select_future_date(browser):
    browser.get("https://www.aviasales.ru/")
    browser.execute_script("""
        window.localStorage.setItem('city', 'IJK');
        window.localStorage.setItem('country', 'RU');
        window.localStorage.setItem('cityName', 'Ижевск');
    """)
    browser.refresh()
    date_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Туда']"))
    )
    date_field.click()
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".Calendar_root"))
    )
    date_cell = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-date='2025-09-21']"))
    )
    date_cell.click()
    browser.find_element(By.TAG_NAME, "body").click()
    WebDriverWait(browser, 20).until(
        lambda d: "21 сентября" in d.find_element(By.CSS_SELECTOR, "input[placeholder='Туда']").get_attribute("value") or "21.09.2025" in d.find_element(By.CSS_SELECTOR, "input[placeholder='Туда']").get_attribute("value")
    )
    value = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Туда']").get_attribute("value")
    assert "21 сентября" in value or "21.09.2025" in value


def test_perform_search_with_valid_data(browser):
    browser.get("https://www.aviasales.ru/")
    browser.execute_script("""
        window.localStorage.setItem('city', 'IJK');
        window.localStorage.setItem('country', 'RU');
        window.localStorage.setItem('cityName', 'Ижевск');
    """)
    browser.refresh()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )
    search_button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_root:has(span:contains('Найти'))"))
    )
    search_button.click()
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".TicketCard_root"))
    )
    title = browser.title.lower()
    assert "билеты" in title or "результаты" in title


def test_search_with_invalid_city(browser):
    browser.get("https://www.aviasales.ru/")
    browser.execute_script("""
        window.localStorage.setItem('city', 'IJK');
        window.localStorage.setItem('country', 'RU');
        window.localStorage.setItem('cityName', 'Ижевск');
    """)
    browser.refresh()
    field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Куда']"))
    )
    field.clear()
    field.send_keys("НесуществующийГород123")
    search_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_root:has(span:contains('Найти'))"))
    )
    search_button.click()
    error_msg = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".ErrorMessage_root"))
    )
    text = error_msg.text.lower()
    assert any(word in text for word in ["не найден", "город", "ошибка"])