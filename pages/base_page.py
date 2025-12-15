import allure

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    OVERLAY = (By.CSS_SELECTOR, "[class*='Modal_modal_overlay']")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу: {url}")
    def open_url(self, url: str):
        self.driver.get(url)

    @allure.step("Найти видимый элемент: {locator}")
    def find_element(self, locator, timeout: int | None = None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Дождаться исчезновения overlay")
    def wait_overlay_gone(self, timeout: int | None = None) -> bool:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.invisibility_of_element_located(self.OVERLAY))
        except TimeoutException:
            return False

    @allure.step("Клик по элементу: {locator}")
    def click_on_element(self, locator, timeout: int | None = None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)

        self.wait_overlay_gone(timeout)

        for _ in range(2):
            try:
                el = wait.until(EC.element_to_be_clickable(locator))
                el.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                self.wait_overlay_gone(timeout)

        el = wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)

    @allure.step("Заполнить поле: {locator}")
    def fill_element(self, locator, value: str, timeout: int | None = None, clear: bool = True):
        el = self.find_element(locator, timeout)
        if clear:
            el.clear()
        el.send_keys(value)

    @allure.step("Получить текущий URL")
    def get_cur_url(self) -> str:
        return self.driver.current_url