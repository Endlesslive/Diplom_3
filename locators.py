from selenium.webdriver.common.by import By

class HeaderLocators:
    CONSTRUCTOR = (By.XPATH, "//a[@href='/']")
    FEED_LINK = (By.XPATH, "//a[@href='/feed']")

class ModalLocators:
    MODAL = (By.CSS_SELECTOR, "section[class*='Modal_modal']")
    OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal__overlay'], div[class*='Modal_modal_overlay']")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")

class MainPageLocators:
    INGREDIENT_CARDS = (By.CSS_SELECTOR, "a[href^='/ingredient/']")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "[class*='counter__num'], [class*='counter_counter__num']")
    CONSTRUCTOR_DROPZONE = (By.CSS_SELECTOR, "section[class*='BurgerConstructor']")
    CONSTRUCTOR_DROPZONE_FALLBACK = (By.XPATH,"//*[contains(.,'Перетащите булочку сюда')]/ancestor::*[self::section or self::div][1]",)
    CONSTRUCTOR_BUTTON = HeaderLocators.CONSTRUCTOR
    ORDER_FEED_BUTTON = HeaderLocators.FEED_LINK
    INGREDIENT = INGREDIENT_CARDS
    CONSTRUCTOR_DROP = CONSTRUCTOR_DROPZONE
    POPUP_WINDOW = ModalLocators.MODAL
    CLOSE_POPUP_BUTTON = ModalLocators.CLOSE_BUTTON
    OVERLAY = ModalLocators.OVERLAY

class LoginPageLocators:
    EMAIL_LOCATOR = (By.XPATH, "//label[contains(normalize-space(),'Email')]/following-sibling::input")
    PASSWORD_LOCATOR = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//button[contains(., 'Войти')]")


class OrderPageLocators:
    FEED_ROOT = (By.CSS_SELECTOR, "div[class*='OrderFeed_orderFeed']")
    ORDERS_LIST = (By.XPATH, "//h1[contains(normalize-space(),'Лента заказов')]/following::ul[1]")
    ORDER_CARD = (By.XPATH, ".//li")
    DONE_SECTION = (By.XPATH, "//*[contains(normalize-space(),'Готовы')]/following::ul[1]")
    IN_PROGRESS_SECTION = (By.XPATH, "//*[contains(normalize-space(),'В работе')]/following::ul[1]")
    IN_PROGRESS_ORDER_NUMBERS = (By.XPATH, "//*[contains(normalize-space(),'В работе')]/following::ul[1]" "//*[contains(@class,'text_type_digits-default')]")
    ORDERS_TOTAL = (By.XPATH,"//*[contains(normalize-space(),'Выполнено за все время')]""/following::*[normalize-space() and translate(normalize-space(.), '0123456789', '') != normalize-space(.)][1]")
    ORDERS_TODAY = (By.XPATH,"//*[contains(normalize-space(),'Выполнено за сегодня')]" "/following::*[normalize-space() and translate(normalize-space(.), '0123456789', '') != normalize-space(.)][1]")
    ORDER_FEED_BUTTON = HeaderLocators.FEED_LINK
    CONSTRUCTOR_BUTTON = HeaderLocators.CONSTRUCTOR
    INGREDIENT = (By.XPATH,"//a[starts-with(@href,'/ingredient/')][.//p[normalize-space()='Флюоресцентная булка R2-D3']]")
    CONSTRUCTOR_DROP = MainPageLocators.CONSTRUCTOR_DROP
    MODAL_CLOSE_BTN = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal__overlay'], div[class*='Modal_modal_overlay']")
    CREATE_ORDER_BUTTON = (By.XPATH, "//button[contains(.,'Оформить заказ')]")
    MODAL_CLOSE_BUTTON = ModalLocators.CLOSE_BUTTON
    NUMBER_OF_ORDER = (By.CSS_SELECTOR, "h2[class*='Modal_modal__title']")
    LIST_NUMBER_OF_ORDER_ON_WORK = (By.XPATH, "//*[contains(normalize-space(),'В работе')]/following::ul[1]//li[1]")
    OVERLAY = ModalLocators.OVERLAY

class FeedPageLocators:
    TOTAL_DONE = OrderPageLocators.ORDERS_TOTAL
    TODAY_DONE = OrderPageLocators.ORDERS_TODAY
    IN_PROGRESS_SECTION = OrderPageLocators.IN_PROGRESS_SECTION

class BasePageLocators:
    OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal__overlay']")
    MODAL_CLOSE_BTN = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")