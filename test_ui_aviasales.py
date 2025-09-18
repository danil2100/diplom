import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure import step, title, description, severity, severity_level


@title("Проверка: город отправления автоматически установлен")
@description("Тест проверяет, что поле 'Откуда' на главной странице Aviasales заполнено автоматически.")
@severity(severity_level.NORMAL)
def test_default_departure_city_is_set(browser):
    """Проверка: город отправления автоматически установлен"""
    with step("Открываем главную страницу Aviasales"):
        browser.get("https://www.aviasales.ru")

    with step("Ожидаем появления поля 'Откуда'"):
        field = WebDriverWait(browser, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Откуда']"))
        )

    with step("Проверяем, что поле содержит значение"):
        value = field.get_attribute("value")
        assert len(value) > 0, "Город отправления не определился"


@title("Проверка: заголовок страницы содержит 'Авиасейлс' или 'Aviasales'")
@description("Тест проверяет, что заголовок браузера содержит ожидаемое название сайта.")
@severity(severity_level.NORMAL)
def test_page_title_contains_aviasales(browser):
    """Проверка: заголовок страницы содержит 'Авиасейлс' или 'Aviasales'"""
    with step("Открываем главную страницу Aviasales"):
        browser.get("https://www.aviasales.ru")

    with step("Ожидаем, что заголовок содержит 'Авиасейлс' или 'Aviasales'"):
        WebDriverWait(browser, 40).until(
            lambda driver: any(word in driver.title for word in ["Авиасейлс", "Aviasales"])
        )

    with step("Проверяем содержимое заголовка"):
        assert any(word in browser.title for word in ["Авиасейлс", "Aviasales"]), \
            f"Ожидалось 'Авиасейлс' или 'Aviasales', получено: {browser.title}"


@title("Проверка: заголовок главной страницы отображается корректно")
@description("Тест проверяет наличие и текст заголовка 'header__title' на главной странице.")
@severity(severity_level.NORMAL)
def test_main_page_header_title(browser):
    """Проверка: заголовок главной страницы отображается корректно"""
    with step("Открываем главную страницу Aviasales"):
        browser.get("https://www.aviasales.ru")

    with step("Ожидаем появления заголовка 'header__title'"):
        header_title = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header__title"))
        )

    with step("Проверяем, что заголовок отображается и содержит ожидаемый текст"):
        assert header_title.is_displayed(), "Заголовок страницы 'header__title' не отображается"
        assert "Тут покупают дешёвые авиабилеты" in header_title.text or "Авиасейлс" in header_title.text, \
            f"Ожидался текст заголовка, получено: '{header_title.text}'"


@title("Проверка: прямой переход на страницу отелей и корректный заголовок")
@description("Тест открывает страницу отелей по URL и проверяет заголовок 'Здесь бронируют балдёжные отели'.")
@severity(severity_level.NORMAL)
def test_open_hotels_page_directly(browser):
    """Проверка: прямой переход на страницу отелей и корректный заголовок"""
    with step("Открываем страницу отелей по URL: /hotels"):
        browser.get("https://www.aviasales.ru/hotels")

    with step("Ожидаем появления заголовка страницы отелей"):
        hotels_header = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Здесь бронируют балдёжные отели')]"))
        )

    with step("Проверяем, что заголовок содержит ожидаемый текст и URL верный"):
        assert "Здесь бронируют балдёжные отели" in hotels_header.text, \
            "На странице отелей нет заголовка 'Здесь бронируют балдёжные отели'"
        assert "/hotels" in browser.current_url, "Не перешли на страницу отелей"


@title("Проверка: прямой переход на страницу 'Короче' (Путеводители) и корректный заголовок")
@description("Тест открывает страницу 'Короче' по URL и проверяет заголовок 'Короче о городах'.")
@severity(severity_level.NORMAL)
def test_open_guides_page_directly(browser):
    """Проверка: прямой переход на страницу 'Короче' (Путеводители) и корректный заголовок"""
    with step("Открываем страницу 'Короче' по URL: /guides"):
        browser.get("https://www.aviasales.ru/guides")

    with step("Ожидаем появления заголовка страницы 'Короче о городах'"):
        korotche_header = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Короче о городах')]"))
        )

    with step("Проверяем, что заголовок содержит ожидаемый текст и URL верный"):
        assert "Короче о городах" in korotche_header.text, \
            "На странице 'Короче' нет заголовка 'Короче о городах'"
        assert "/guides" in browser.current_url, "Не перешли на страницу 'Короче'"