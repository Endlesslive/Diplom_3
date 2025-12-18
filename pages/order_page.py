import allure
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from locators import OrderPageLocators, LoginPageLocators, BasePageLocators
import urls


class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @staticmethod
    def _digits(text: str) -> str:
        return "".join(ch for ch in text if ch.isdigit())

    def wait_feed_loaded(self, timeout: int = 40):
        self.wait_url_contains(urls.URL_FEED, timeout)
        self.wait_element_present(OrderPageLocators.FEED_ROOT, timeout)

    @allure.step("Логин")
    def login(self, email, password):
        self.open_url(urls.URL_LOGIN)
        self.fill_element(LoginPageLocators.EMAIL_LOCATOR, email)
        self.fill_element(LoginPageLocators.PASSWORD_LOCATOR, password)
        self.click_on_element(LoginPageLocators.LOGIN_BUTTON_LOCATOR)
        self.wait_url_contains(urls.MAIN_URL)

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
        self.wait_url_contains(urls.MAIN_URL)

    @allure.step('Перетащить элемент в корзину')
    def put_ingredient_into_basket(self):
        self.wait_url_contains(urls.MAIN_URL)
        ingredient = self.wait_element_clickable(OrderPageLocators.INGREDIENT)
        basket = self.find_element(OrderPageLocators.CONSTRUCTOR_DROP)
        
        self.scroll_into_view(ingredient)
        time.sleep(0.3)

        actions = ActionChains(self.driver)
        actions.move_to_element(ingredient).click_and_hold()
        actions.move_to_element(basket).release().perform()
        
        self.wait_condition(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "[class*='constructor-element']")) > 0,
            timeout=10
        )
        self.wait_element_clickable(OrderPageLocators.CREATE_ORDER_BUTTON, timeout=30)

    @allure.step("Оформить заказ")
    def click_on_order_button(self):
        self.wait_element_invisible(BasePageLocators.OVERLAY, timeout=10)
        self.click_on_element(OrderPageLocators.CREATE_ORDER_BUTTON)
        self.wait_element_present(OrderPageLocators.NUMBER_OF_ORDER, timeout=30)

    @allure.step("Получить номер заказа из модалки")
    def get_number_of_order(self) -> str:
        el = self.wait_element_present(OrderPageLocators.NUMBER_OF_ORDER, timeout=30)
        self.wait_condition(lambda d: self._digits(el.text) != "", timeout=30)
        return self._digits(el.text)

    @allure.step("Закрыть модалку заказа")
    def click_on_close_window_button(self):
        self.wait_overlay_gone()
        try:
            self.click_on_element(BasePageLocators.MODAL_CLOSE_BTN)
        except Exception:
            pass
        try:
            btn = self.wait_element_present(BasePageLocators.MODAL_CLOSE_BTN)
            self.click_via_js(btn)
        except Exception:
            pass
        self.wait_element_invisible(BasePageLocators.OVERLAY, timeout=15)
        self.wait_overlay_gone()

    @allure.step("Счетчик заказов за все время")
    def get_total_orders(self) -> str:
        self.wait_feed_loaded(timeout=40)
        el = self.wait_element_present(OrderPageLocators.ORDERS_TOTAL, timeout=40)
        self.wait_condition(lambda d: self._digits(el.text) != "", timeout=40)
        return self._digits(el.text)

    @allure.step("Счетчик заказов за сегодня")
    def get_today_orders(self) -> str:
        self.wait_feed_loaded(timeout=40)
        el = self.wait_element_present(OrderPageLocators.ORDERS_TODAY, timeout=40)
        self.wait_condition(lambda d: self._digits(el.text) != "", timeout=40)
        return self._digits(el.text)

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator, timeout: int | None = None):
        """Находит все элементы по локатору"""
        self.wait_element_present(locator, timeout)
        return self.driver.find_elements(*locator)

    @allure.step("Номера заказов в 'В работе' (список)")
    def get_orders_in_progress_numbers(self) -> list[str]:
        self.wait_feed_loaded(timeout=40)
        els = self.find_elements(OrderPageLocators.IN_PROGRESS_ORDER_NUMBERS)
        return [self._digits(e.text) for e in els if self._digits(e.text)]

    @allure.step("Ожидание увеличения счетчика {counter_type}")
    def wait_for_counter_increase(self, initial_value, counter_type='total', timeout=60):
        def _counter_increased(driver):
            if counter_type == 'total':
                current = int(self.get_total_orders())
            else:
                current = int(self.get_today_orders())
            return current > initial_value
        
        self.wait_condition(_counter_increased, timeout=timeout)