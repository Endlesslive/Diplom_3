import allure

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import BasePageLocators


class BasePage:
    # Константы для переиспользования
    OVERLAY = BasePageLocators.OVERLAY
    MODAL_CLOSE_BTN = BasePageLocators.MODAL_CLOSE_BTN
    
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу: {url}")
    def open_url(self, url: str):
        self.driver.get(url)

    @allure.step("Получить текущий URL")
    def get_cur_url(self) -> str:
        return self.driver.current_url

    @allure.step("Создать WebDriverWait с таймаутом {timeout}")
    def get_wait(self, timeout: int | None = None):
        """Создаёт WebDriverWait с указанным таймаутом"""
        return self.wait if timeout is None else WebDriverWait(self.driver, timeout)

    @allure.step("Выполнить JavaScript: {script}")
    def execute_script(self, script: str, *args):
        """Выполняет JavaScript в контексте браузера"""
        return self.driver.execute_script(script, *args)

    @allure.step("Прокрутить элемент в центр экрана")
    def scroll_into_view(self, element):
        """Прокручивает элемент в видимую область (центр экрана)"""
        self.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    @allure.step("Кликнуть по элементу через JavaScript")
    def click_via_js(self, element):
        """Выполняет клик по элементу через JavaScript"""
        self.execute_script("arguments[0].click();", element)

    @allure.step("Найти видимый элемент: {locator}")
    def find_element(self, locator, timeout: int | None = None):
        wait = self.get_wait(timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator, timeout: int | None = None):
        """Находит все элементы по локатору (после ожидания первого)"""
        self.wait_element_present(locator, timeout)
        return self.driver.find_elements(*locator)

    @allure.step("Дождаться присутствия элемента: {locator}")
    def wait_element_present(self, locator, timeout: int | None = None):
        """Ждёт появления элемента в DOM (не обязательно видимого)"""
        wait = self.get_wait(timeout)
        return wait.until(EC.presence_of_element_located(locator))

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_element_clickable(self, locator, timeout: int | None = None):
        """Ждёт, пока элемент станет кликабельным"""
        wait = self.get_wait(timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Дождаться исчезновения элемента: {locator}")
    def wait_element_invisible(self, locator, timeout: int | None = None):
        """Ждёт исчезновения элемента"""
        wait = self.get_wait(timeout)
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False

    @allure.step("Дождаться исчезновения overlay")
    def wait_overlay_gone(self, timeout: int | None = None) -> bool:
        return self.wait_element_invisible(BasePageLocators.OVERLAY, timeout)

    @allure.step("Дождаться выполнения условия")
    def wait_condition(self, condition, timeout: int | None = None):
        """Ждёт выполнения произвольного условия (lambda)"""
        wait = self.get_wait(timeout)
        return wait.until(condition)

    @allure.step("Дождаться URL содержит: {url_part}")
    def wait_url_contains(self, url_part: str, timeout: int | None = None):
        """Ждёт, пока URL будет содержать указанную часть"""
        wait = self.get_wait(timeout)
        return wait.until(EC.url_contains(url_part))

    @allure.step("Дождаться точного URL: {url}")
    def wait_url_to_be(self, url: str, timeout: int | None = None):
        """Ждёт, пока URL станет точно равен указанному"""
        wait = self.get_wait(timeout)
        return wait.until(EC.url_to_be(url))

    @allure.step("Дождаться изменения URL")
    def wait_url_changes(self, old_url: str, timeout: int | None = None):
        """Ждёт, пока URL изменится"""
        wait = self.get_wait(timeout)
        return wait.until(EC.url_changes(old_url))

    @allure.step("Клик по элементу: {locator}")
    def click_on_element(self, locator, timeout: int | None = None):
        self.wait_overlay_gone(timeout)

        for _ in range(2):
            try:
                el = self.wait_element_clickable(locator, timeout)
                el.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                self.wait_overlay_gone(timeout)

        el = self.wait_element_present(locator, timeout)
        self.scroll_into_view(el)
        self.click_via_js(el)

    @allure.step("Заполнить поле: {locator}")
    def fill_element(self, locator, value: str, timeout: int | None = None, clear: bool = True):
        el = self.find_element(locator, timeout)
        if clear:
            el.clear()
        el.send_keys(value)

    @allure.step("Получить текст элемента: {locator}")
    def get_element_text(self, locator, timeout: int | None = None) -> str:
        """Возвращает текст элемента"""
        element = self.find_element(locator, timeout)
        return element.text

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator, timeout: int = 2) -> bool:
        """Проверяет, виден ли элемент (с обработкой исключений)"""
        try:
            wait = self.get_wait(timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except Exception:
            return False
