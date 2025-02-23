from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.order_locators import OrderLocators
from locators.profile_locators import ProfileLocators
from pages.profile_page import ProfilePage
from pages.order_history_page import OrderPage
from pages.constructor_page import ConstructorPage
from locators.constructor_locators import ConstructorLocators
from pages.url import MAIN_PAGE_URL, ORDER_HISTORY_URL, PROFILE_URL, FEED_URL
import allure

class TestOrderPage:

    @allure.title("Открытие деталей заказа из истории заказов")
    def test_open_order_details(self, driver):
        profile_page = ProfilePage(driver)
        order_history_page = OrderPage(driver)

        profile_page.go_to_login_page()
        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)

        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)
        WebDriverWait(driver, 10).until(EC.url_to_be(PROFILE_URL))

        profile_page.click_to_element(ProfileLocators.ORDER_HISTORY_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(ORDER_HISTORY_URL))

        order_history_page.click_to_element(OrderLocators.LAST_ORDER)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(OrderLocators.ORDER_DETAILS_MODAL))

        order_number = order_history_page.get_text_from_element(OrderLocators.ORDER_NUMBER_IN_MODAL)
        assert order_number == "#0183759", f"Ожидаемый номер заказа '#0183759', но найден {order_number}"

    @allure.title("Проверка перехода из истории заказов в ленту заказов")
    def test_orders_from_history_to_feed(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        profile_page.go_to_login_page()
        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))
        initial_counter_value = constructor_page.get_counter_value()
        constructor_page.drag_ingredient_to_order(ConstructorLocators.ELEMENT_INGREDIENT,ConstructorLocators.ORDER_BLOCK)
        new_counter_value = constructor_page.get_counter_value()

        constructor_page.click_order_button()

        order_number_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(OrderLocators.ORDER_NUMBER_POPUP))
        WebDriverWait(driver, 30).until(lambda d: d.find_element(*OrderLocators.ORDER_NUMBER_POPUP).text != "9999")
        expected_order_number = order_number_element.text

        constructor_page.click_to_element(OrderLocators.CLOSE_POPUP_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))


        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)
        profile_page.click_to_element(ProfileLocators.ORDER_HISTORY_BUTTON)

        WebDriverWait(driver, 30).until(lambda d: len(d.find_elements(*OrderLocators.NUMBERS_ORDER)) > 0)

        order_from_history = order_page.get_last_order_history()

        order_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(OrderLocators.NUMBERS_ORDER))

        assert order_page.get_check_number_order(order_from_history)

    @allure.title("Проверка увеличения счетчика выполненных заказов после создания нового заказа")
    def test_create_order_increases_completed_orders_counter(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        profile_page.go_to_login_page()
        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        order_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(OrderLocators.COUNTER_DONE_ALL_TIME)
        )

        initial_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_ALL_TIME)

        order_page.click_to_element(ConstructorLocators.CONSTRUCTOR_PAGE)
        initial_counter_value = constructor_page.get_counter_value()
        constructor_page.drag_ingredient_to_order(ConstructorLocators.ELEMENT_INGREDIENT,ConstructorLocators.ORDER_BLOCK)
        new_counter_value = constructor_page.get_counter_value()
        constructor_page.click_order_button()
        constructor_page.click_to_element(OrderLocators.CLOSE_POPUP_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        order_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(OrderLocators.COUNTER_DONE_ALL_TIME))

        new_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_ALL_TIME)

        assert new_counter_value > initial_counter_value, f"Счетчик заказов не увеличился: было {initial_counter_value}, стало {new_counter_value}"

    @allure.title("Проверка увеличения счетчика выполненных заказов за сегодняшний день после создания нового заказа")
    def test_create_order_increases_today_counter(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        profile_page.go_to_login_page()
        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        order_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(OrderLocators.COUNTER_DONE_TODAY))

        initial_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_TODAY)

        order_page.click_to_element(ConstructorLocators.CONSTRUCTOR_PAGE)
        initial_counter_value = constructor_page.get_counter_value()
        constructor_page.drag_ingredient_to_order(ConstructorLocators.ELEMENT_INGREDIENT,ConstructorLocators.ORDER_BLOCK)
        new_counter_value = constructor_page.get_counter_value()
        constructor_page.click_order_button()
        constructor_page.click_to_element(OrderLocators.CLOSE_POPUP_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        order_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(OrderLocators.COUNTER_DONE_TODAY))

        new_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_TODAY)
        assert new_counter_value > initial_counter_value, f"Счетчик заказов не увеличился: было {initial_counter_value}, стало {new_counter_value}"

    @allure.title("Проверка появления номера заказа в разделе 'В работе' после создания заказа")
    def test_order_number_appears_in_in_progress_after_order_creation(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        profile_page.go_to_login_page()
        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        initial_counter_value = constructor_page.get_counter_value()
        constructor_page.drag_ingredient_to_order(ConstructorLocators.ELEMENT_INGREDIENT,ConstructorLocators.ORDER_BLOCK)
        new_counter_value = constructor_page.get_counter_value()

        constructor_page.click_order_button()

        order_number_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(OrderLocators.ORDER_NUMBER_POPUP))
        WebDriverWait(driver, 30).until(lambda d: d.find_element(*OrderLocators.ORDER_NUMBER_POPUP).text != "9999")
        expected_order_number = order_number_element.text

        constructor_page.click_to_element(OrderLocators.CLOSE_POPUP_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        order_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 20).until(EC.url_to_be(FEED_URL))

        expected_order_number = str(expected_order_number).zfill(7)

        WebDriverWait(driver, 30).until(
            lambda d: any(expected_order_number in el.text for el in d.find_elements(*OrderLocators.ORDER_IN_PROGRESS)),
            message=f"Номер заказа {expected_order_number} не появился в разделе 'В работе'"
        )

        order_numbers = order_page.get_orders_in_progress()

        assert expected_order_number in order_numbers, f"Номер заказа {expected_order_number} не найден в 'В работе'. Найденные номера: {order_numbers}"
