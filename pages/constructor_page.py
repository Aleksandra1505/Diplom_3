from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePageMetod
from locators.constructor_locators import ConstructorLocators
import allure

class ConstructorPage(BasePageMetod):

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

    @allure.step('Открытие всплывающего окна ингредиента')
    def open_ingredient_info(self):
        self.click_to_element(ConstructorLocators.ELEMENT_INGREDIENT)
        return self.is_element_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.step('Закрытие всплывающего окна ингредиента')
    def close_ingredient_info(self):
        self.click_to_element(ConstructorLocators.BUTTON_CLOSE_INFO_INGREDIENT)
        return self.is_element_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.step('Добавление ингредиента в заказ')
    def add_ingredient_to_order(self):
        counter_before = self.get_counter_value()
        self.click_to_element(ConstructorLocators.ELEMENT_INGREDIENT)
        counter_after = self.get_counter_value()
        return counter_after > counter_before

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

    @allure.step('Клик по кнопке Оформить заказ')
    def click_order_button(self):
        self.click_to_element(ConstructorLocators.ORDER_BUTTON)

    @allure.step('Проверяем, что появился попап с подтверждением заказа')
    def is_order_confirmation_displayed(self):
        return self.is_element_visible(ConstructorLocators.ORDER_CONFIRMATION_POPUP)