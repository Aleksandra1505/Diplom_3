from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.constructor_page import ConstructorPage
from locators.constructor_locators import ConstructorLocators
from locators.profile_locators import ProfileLocators
from pages.profile_page import ProfilePage
from pages.url import MAIN_PAGE_URL, FEED_URL
import allure

class TestConstructor:
    @allure.title("Переход на страницу конструктора")
    def test_go_to_constructor(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_main_page()

        constructor_page.click_to_element(ConstructorLocators.CONSTRUCTOR_PAGE)

        assert driver.current_url == MAIN_PAGE_URL

    @allure.title("Переход на Ленту заказов")
    def test_go_to_orders_feed(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_main_page()

        constructor_page.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)

        assert driver.current_url == FEED_URL

    @allure.title("Открытие попапа с информацией об ингредиенте")
    def test_ingredient_info_popup(self, driver):
        constructor_page = ConstructorPage(driver)
        constructor_page.open_main_page()

        constructor_page.open_ingredient_info()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ConstructorLocators.INFO_INGREDIENT))

        assert constructor_page.is_element_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.title("Закрытие попапа с информацией об ингредиенте по клику на крестик")
    def test_close_ingredient_info_popup_by_clicking_cross(self, driver):
        constructor_page = ConstructorPage(driver)

        constructor_page.open_main_page()

        constructor_page.open_ingredient_info()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(ConstructorLocators.INFO_INGREDIENT))

        constructor_page.close_ingredient_info()
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(ConstructorLocators.INFO_INGREDIENT))

        assert constructor_page.is_element_not_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.title("Добавление ингредиента в заказ увеличивает счетчик")
    def test_add_ingredient_to_order(self, driver):
        constructor_page = ConstructorPage(driver)

        constructor_page.open_main_page()
        WebDriverWait(driver, 4).until(EC.url_to_be(MAIN_PAGE_URL))

        initial_counter_value = constructor_page.get_counter_value()

        constructor_page.drag_ingredient_to_order(ConstructorLocators.ELEMENT_INGREDIENT, ConstructorLocators.ORDER_BLOCK)


        new_counter_value = constructor_page.get_counter_value()

        assert new_counter_value > initial_counter_value

    @allure.title("Добавление ингредиента в заказ и оформление заказа с подтверждением")
    def test_add_order(self, driver):
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        profile_page.go_to_login_page()
        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)

        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        initial_counter_value = constructor_page.get_counter_value()

        constructor_page.drag_ingredient_to_order(ConstructorLocators.ELEMENT_INGREDIENT,
                                                  ConstructorLocators.ORDER_BLOCK)

        new_counter_value = constructor_page.get_counter_value()

        assert new_counter_value > initial_counter_value, "Ингредиент не добавился в заказ"

        constructor_page.click_order_button()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(ConstructorLocators.ORDER_CONFIRMATION_POPUP)
        )

        assert constructor_page.is_order_confirmation_displayed(), "Попап с подтверждением заказа не появился"

