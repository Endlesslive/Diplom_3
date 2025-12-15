import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from locators import MainPageLocators
import urls


class MainPage(BasePage):

    @allure.step("Открытие страницы логина")
    def open_login_page(self):
        self.open_url(urls.URL_LOGIN)
        self.wait.until(EC.url_to_be(urls.URL_LOGIN))

    @allure.step("Открытие страницы конструктора")
    def open_main_page(self):
        self.open_url(urls.MAIN_URL)
        self.wait.until(EC.url_to_be(urls.MAIN_URL))

    @allure.step("Клик на кнопку Конструктор")
    def click_to_open_constructor_page(self):
        self.click_on_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        self.wait.until(EC.url_contains(urls.MAIN_URL))

    @allure.step("Клик на кнопку Лента заказов")
    def click_on_order_button(self):
        self.click_on_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.wait.until(EC.url_contains(urls.URL_FEED))

    @allure.step("Открыть попап ингредиента")
    def click_on_ingredient(self):
        self.click_on_element(MainPageLocators.INGREDIENT)

    @allure.step("Закрыть попап ингредиента")
    def click_on_close_popup_button(self):
        self.click_on_element(MainPageLocators.CLOSE_POPUP_BUTTON)
        self.wait_overlay_gone()

    @allure.step("Проверить попап ингредиента")
    def check_popup_window(self):
        try:
            return self.find_element(MainPageLocators.POPUP_WINDOW).is_displayed()
        except Exception:
            return False

    @allure.step("Получить счетчик ингредиента")
    def get_ingredient_counter(self):
        return self.find_element(MainPageLocators.INGREDIENT_COUNTER).text

    @allure.step("DnD ингредиента в корзину (JS)")
    def put_ingredient_into_basket(self):
        self.wait.until(EC.url_to_be(urls.MAIN_URL))

        source = self.find_element(MainPageLocators.INGREDIENT)
        target = self.find_element(MainPageLocators.CONSTRUCTOR_DROP)

        before = self.get_ingredient_counter().strip()

        js = """
        const source = arguments[0];
        const target = arguments[1];
        const dataTransfer = new DataTransfer();
        function fire(type, elem) {
          const event = new DragEvent(type, { bubbles: true, cancelable: true, dataTransfer });
          elem.dispatchEvent(event);
        }
        fire('dragstart', source);
        fire('dragenter', target);
        fire('dragover', target);
        fire('drop', target);
        fire('dragend', source);
        """
        self.driver.execute_script(js, source, target)

        WebDriverWait(self.driver, 10).until(lambda d: self.get_ingredient_counter().strip() != before)
