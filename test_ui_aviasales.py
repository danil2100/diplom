import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_default_departure_city_is_set(browser):
    """Проверка: город отправления автоматически установлен"""
    browser.get("https://www.aviasales.ru")
    field = WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )
    value = field.get_attribute("value")
    assert len(value) > 0, "Город отправления не определился"


def test_page_title_contains_aviasales(browser):
    """Проверка: заголовок страницы содержит 'Авиасейлс' или 'Aviasales'"""
    browser.get("https://www.aviasales.ru")
    WebDriverWait(browser, 40).until(
        lambda driver: any(word in driver.title for word in ["Авиасейлс", "Aviasales"])
    )
    assert any(word in browser.title for word in ["Авиасейлс", "Aviasales"]), \
        f"Ожидалось 'Авиасейлс' или 'Aviasales', получено: {browser.title}"


def test_scroll_to_bottom_and_return(browser):
    """Проверка: прокрутка до конца страницы и возврат в начало"""
    browser.get("https://www.aviasales.ru")

    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )

    # Прокручиваем вниз
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    return_button = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='choose-destination-on-button']"))
    )
    return_button.click()

    # Проверяем, что вернулись к полю "Откуда"
    from_field = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )
    assert from_field.is_displayed(), "Поле 'Откуда' должно быть видимым после возврата"


def test_switch_to_hotels_tab(browser):
    """Проверка: переход на вкладку 'Отели'"""
    browser.get("https://www.aviasales.ru")

    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )

    # ✅ Правильный селектор: <a> с href="/hotels", внутри которого есть div с текстом "Отели"
    hotels_link = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/hotels'][.//div[text()='Отели']]"))
    )
    hotels_link.click()

    WebDriverWait(browser, 30).until(
        EC.url_contains("/hotels")
    )
    assert "/hotels" in browser.current_url, "Не перешли на страницу отелей"


def test_switch_to_korotche_tab(browser):
    """Проверка: переход на вкладку 'Короче'"""
    browser.get("https://www.aviasales.ru")

    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )

    korotche_link = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/korotche'][.//div[text()='Короче']]"))
    )
    korotche_link.click()

    WebDriverWait(browser, 30).until(
        EC.url_contains("/korotche")
    )
    assert "/korotche" in browser.current_url, "Не перешли на страницу 'Короче'"
    """Проверка: переход на вкладку 'Короче'"""
    browser.get("https://www.aviasales.ru")

    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
    )

    korotche_link = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/korotche'][.//div[text()='Короче']]"))
    )
    korotche_link.click()

    WebDriverWait(browser, 30).until(
        EC.url_contains("/korotche")
    )
    assert "/korotche" in browser.current_url, "Не перешли на страницу 'Короче'"