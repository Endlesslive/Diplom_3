import allure
from selenium.webdriver.support.ui import WebDriverWait

from pages.order_page import OrderPage
from data import UsersTestData


class TestOrderFeed:

    @allure.title("Увеличение счетчиков заказов за все время")
    def test_go_to_order_total(self, driver):
        page = OrderPage(driver)
        page.login(UsersTestData.email, UsersTestData.password)

        page.open_feed_page()
        first = int(page.get_total_orders())

        page.click_on_constructor_button()
        page.put_ingredient_into_basket()
        page.click_on_order_button()
        page.click_on_close_window_button()

        page.open_feed_page()
        page.wait_for_counter_increase(first, 'total', timeout=60)
        second = int(page.get_total_orders())

        assert first < second

    @allure.title("Увеличение счетчиков заказов за сегодня")
    def test_go_to_order_today(self, driver):
        page = OrderPage(driver)
        page.login(UsersTestData.email, UsersTestData.password)

        page.open_feed_page()
        first = int(page.get_today_orders())

        page.click_on_constructor_button()
        page.put_ingredient_into_basket()
        page.click_on_order_button()
        page.click_on_close_window_button()

        page.open_feed_page()
        page.wait_for_counter_increase(first, 'today', timeout=90)
        second = int(page.get_today_orders())

        assert first < second

    @allure.title("Заказ в работе")
    def test_is_order_in_progress(self, driver):
        page = OrderPage(driver)
        page.login(UsersTestData.email, UsersTestData.password)

        page.click_on_constructor_button()
        page.put_ingredient_into_basket()
        page.click_on_order_button()
        page.click_on_close_window_button()

        page.open_feed_page()
        assert page.get_orders_in_progress_numbers(), "Секция 'В работе' пустая"
