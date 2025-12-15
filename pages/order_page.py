import allure
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from locators import OrderPageLocators, LoginPageLocators
import urls


class OrderPage(BasePage):
    MODAL_CLOSE_BTN = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal__overlay'], div[class*='Modal_modal_overlay']")

    def __init__(self, driver):
        super().__init__(driver)

    @staticmethod
    def _digits(text: str) -> str:
        return "".join(ch for ch in text if ch.isdigit())

    def wait_feed_loaded(self, timeout: int = 40):
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(urls.URL_FEED))
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(OrderPageLocators.FEED_ROOT))

    @allure.step("Логин")
    def login(self, email, password):
        self.open_url(urls.URL_LOGIN)
        self.fill_element(LoginPageLocators.EMAIL_LOCATOR, email)
        self.fill_element(LoginPageLocators.PASSWORD_LOCATOR, password)
        self.click_on_element(LoginPageLocators.LOGIN_BUTTON_LOCATOR)
        self.wait.until(EC.url_contains(urls.MAIN_URL))

    @allure.step("Клик на кнопку Лента заказов")
    def click_on_feed_button(self):
        self.click_on_element(OrderPageLocators.ORDER_FEED_BUTTON)
        self.wait_feed_loaded(timeout=40)

    @allure.step("Открыть ленту заказов")
    def open_feed_page(self):
        self.open_url(urls.URL_FEED)
        self.wait_feed_loaded(timeout=40)

    @allure.step("Клик на кнопку Конструктор")
    def click_on_constructor_button(self):
        self.click_on_element(OrderPageLocators.CONSTRUCTOR_BUTTON)
        self.wait.until(EC.url_contains(urls.MAIN_URL))

    @allure.step('Перетащить элемент в корзину')
    def put_ingredient_into_basket(self):
        self.wait.until(EC.url_to_be(urls.MAIN_URL))
        ingredient = self.wait.until(EC.element_to_be_clickable(OrderPageLocators.INGREDIENT))
        basket = self.wait.until(EC.visibility_of_element_located(OrderPageLocators.CONSTRUCTOR_DROP))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", ingredient)
        time.sleep(0.3)

        actions = ActionChains(self.driver)
        actions.move_to_element(ingredient).click_and_hold()
        actions.move_to_element(basket).release().perform()
        
        WebDriverWait(self.driver, 10).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "[class*='constructor-element']")) > 0)

        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(OrderPageLocators.CREATE_ORDER_BUTTON))

    @allure.step("Оформить заказ")
    def click_on_order_button(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.MODAL_OVERLAY))
        except TimeoutException:
            pass

        self.click_on_element(OrderPageLocators.CREATE_ORDER_BUTTON)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(OrderPageLocators.NUMBER_OF_ORDER))

    @allure.step("Получить номер заказа из модалки")
    def get_number_of_order(self) -> str:
        el = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(OrderPageLocators.NUMBER_OF_ORDER))
        WebDriverWait(self.driver, 30).until(lambda d: self._digits(el.text) != "")
        return self._digits(el.text)

    @allure.step("Закрыть модалку заказа")
    def click_on_close_window_button(self):
        self.wait_overlay_gone()
        try:
            self.click_on_element(self.MODAL_CLOSE_BTN)
        except Exception:
            pass
        try:
            btn = self.driver.find_element(*self.MODAL_CLOSE_BTN)
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass
        try:
            WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located(self.MODAL_OVERLAY))
        except TimeoutException:
            pass
        self.wait_overlay_gone()

    @allure.step("Счетчик заказов за все время")
    def get_total_orders(self) -> str:
        self.wait_feed_loaded(timeout=40)
        el = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located(OrderPageLocators.ORDERS_TOTAL))
        WebDriverWait(self.driver, 40).until(lambda d: self._digits(el.text) != "")
        return self._digits(el.text)

    @allure.step("Счетчик заказов за сегодня")
    def get_today_orders(self) -> str:
        self.wait_feed_loaded(timeout=40)
        el = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located(OrderPageLocators.ORDERS_TODAY)
        )
        WebDriverWait(self.driver, 40).until(lambda d: self._digits(el.text) != "")
        return self._digits(el.text)

    @allure.step("Номера заказов в 'В работе' (список)")
    def get_orders_in_progress_numbers(self) -> list[str]:
        self.wait_feed_loaded(timeout=40)
        els = self.driver.find_elements(*OrderPageLocators.IN_PROGRESS_ORDER_NUMBERS)
        return [self._digits(e.text) for e in els if self._digits(e.text)]
