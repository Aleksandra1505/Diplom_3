from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from locators.constructor_locators import ConstructorLocators
from locators.order_locators import OrderLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class ConstructorPage(BasePage):
    @allure.step('Переход по клику на «Конструктор»')
    def go_to_constructor(self):
        self.click_to_element(ConstructorLocators.CONSTRUCTOR_PAGE)

    @allure.step('Проверка, что заголовок Соберите бургер отображается')
    def is_constructor_header_visible(self):
        return self.is_element_visible(ConstructorLocators.CONSTRUCTOR_HEADER)

    @allure.step('Переход по клику на Лента заказов')
    def go_to_orders_feed(self):
        self.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)

    @allure.step('Проверка, что заголовок Лента заказов отображается')
    def is_orders_feed_visible(self):
        return self.is_element_visible(ConstructorLocators.LIST_ORDER_FEED)

    @allure.step('Получение текущего значения счетчика ингредиента')
    def get_counter_value(self):
        counter_elements = self.get_elements(ConstructorLocators.COUNTER_INGREDIENT)
        return int(counter_elements[0].text) if counter_elements else 0

    @allure.step('Перенос ингредиента')
    def drag_ingredient_to_order(self, source_locator, target_locator):
        source_element = self.wait_for_element(source_locator)
        target_element = self.wait_for_element(target_locator)
        print(f"Элемент для перетаскивания: {source_element}, целевой элемент: {target_element}")  # Логируем элементы
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, target_element).perform()
        print("Перетаскивание выполнено")

    @allure.step('Проверить количество ингредиентов до добавления в корзину')
    def check_count_before_ingredient_added(self):
        return self.get_text_from_element(ConstructorLocators.COUNTER_INGREDIENT)

    @allure.step('Проверяем, что появился попап с подтверждением заказа')
    def is_order_confirmation_displayed(self):
        return self.is_element_visible(ConstructorLocators.ORDER_CONFIRMATION_POPUP)

    """Ниже собраны новые методы, созданные в рамках доработок"""
    @allure.step('Переход на страницу конструктора')
    def go_to_constructor_page(self):
        self.click_to_element(ConstructorLocators.CONSTRUCTOR_PAGE)

    @allure.step('Переход на страницу конструктора')
    def go_to_orders_feed_page(self, driver):
        self.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(OrderLocators.COUNTER_DONE_ALL_TIME)
        )

    @allure.step('Открытие всплывающего окна ингредиента')
    def open_ingredient_info(self):
        self.click_to_element(ConstructorLocators.ELEMENT_INGREDIENT)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(ConstructorLocators.INFO_INGREDIENT))
        return self.is_element_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.step('Закрытие всплывающего окна ингредиента')
    def close_ingredient_info(self):
        self.click_to_element(ConstructorLocators.BUTTON_CLOSE_INFO_INGREDIENT)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(ConstructorLocators.INFO_INGREDIENT))
        return self.is_element_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.step('Добавление ингредиента в заказ')
    def add_ingredient_to_order(self):
        ingredient_locator = ConstructorLocators.ELEMENT_INGREDIENT
        order_block_locator = ConstructorLocators.ORDER_BLOCK
        self.drag_ingredient_to_order(ingredient_locator, order_block_locator)

    @allure.step('Получение начального значения счетчика ингредиента')
    def get_initial_counter_value(self):
        return self.get_counter_value()

    @allure.step('Получение нового значения счетчика ингредиента')
    def get_new_counter_value(self):
        return self.get_counter_value()

    @allure.step('Клик по кнопке Оформить заказ')
    def click_order_button(self):
        self.click_to_element(ConstructorLocators.ORDER_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(ConstructorLocators.ORDER_CONFIRMATION_POPUP))

    @allure.step('Ожидание обновления счетчика выполненных заказов')
    def wait_for_counter_update(self, driver, initial_counter_value):
        WebDriverWait(driver, 20).until(
            lambda driver: self.get_counter_value(OrderLocators.COUNTER_DONE_ALL_TIME) > initial_counter_value
        )

