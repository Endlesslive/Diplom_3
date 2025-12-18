import allure
import locators
import urls
from pages.main_page import MainPage


class TestMainPage:

    @allure.title("Проверка открытия страницы конструктора кликом на кнопку")
    def test_click_on_constructor_button(self, driver):
        main_page = MainPage(driver)
        main_page.open_login_page()
        main_page.click_to_open_constructor_page()
        assert main_page.get_cur_url() == urls.MAIN_URL

    @allure.title("Проверка открытия страницы заказов кликом на кнопку")
    def test_click_on_order_button(self, driver):
        main_page = MainPage(driver)
        main_page.open_login_page()
        main_page.click_on_order_button()
        assert main_page.get_cur_url() == urls.URL_FEED

    @allure.title("Проверка открытия окна попапа ингредиента")
    def test_open_popup_ingredient(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_on_element(locators.MainPageLocators.INGREDIENT)
        assert main_page.check_popup_window()

    @allure.title("Проверка закрытия окна попапа кликом на крестик")
    def test_close_popup_ingredient(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_on_ingredient()
        main_page.click_on_close_popup_button()
        assert not main_page.check_popup_window()

    @allure.title("Проверка увеличения счетчика ингредиента")
    def test_change_ingredient_counter(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        initial_count = int(main_page.get_ingredient_counter())
        main_page.put_ingredient_into_basket()
        new_count = int(main_page.get_ingredient_counter())
        assert new_count > initial_count
