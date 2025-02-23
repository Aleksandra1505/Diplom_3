from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePageMetod
from selenium.webdriver.common.by import By
from locators.order_locators import OrderLocators
from selenium.webdriver.common.action_chains import ActionChains
import allure

class OrderPage(BasePageMetod):
    @allure.step("Открываем детали заказа")
    def open_order_details(self):
        self.click_to_element(OrderLocators.NUMBERS_ORDER)
        return self.is_element_visible(OrderLocators.ORDER_DETAILS_MODAL)

    @allure.step("Проверяем, что номер заказа отображается в ленте заказов")
    def is_order_in_history(self):
        return self.is_element_visible(OrderLocators.NUMBERS_ORDER)

    @allure.step("Получаем количество выполненных заказов за всё время")
    def get_done_orders_count_all_time(self):
        return int(self.get_text_from_element(OrderLocators.COUNTER_DONE_ALL_TIME))

    @allure.step("Получаем количество выполненных заказов за сегодня")
    def get_done_orders_count_today(self):
        return int(self.get_text_from_element(OrderLocators.COUNTER_DONE_TODAY))

    @allure.step("Проверяем, что заказ находится в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        locator = self.format_locators(OrderLocators.ORDER_IN_PROGRESS, order_number)
        return self.is_element_visible(locator)

    @allure.step("Получение списка заказов из истории")
    def get_orders_from_history(self):
        # Ждем, пока элемент "История заказов" не станет видимым
        WebDriverWait(self.driver, 20).until(
            lambda driver: driver.find_element(By.XPATH, '//*[contains(text(), "История заказов")]').is_displayed())
        # Получаем список заказов
        orders = self.driver.find_elements(By.XPATH, '//div[@class="order-history-item"]')
        return [order.text for order in orders]

    @allure.step('Получить кликабельный элемент')
    def find_clickable_element(self, locator):
        WebDriverWait(self.driver, 200).until(lambda driver: driver.find_element(*locator).is_displayed())
        return self.driver.find_element(*locator)

    @allure.step('Получаем все элементы заказов в ленте заказов')
    def get_orders_from_feed(self):
        order_elements = self.driver.find_elements(*OrderLocators.NUMBERS_ORDER)
        orders = []
        for order in order_elements:
            order_number = order.text
            orders.append({"number": order_number})
        return orders

    @allure.step('Получить кликабельный элемент')
    def find_all_elements(self, locator):
        self.find_clickable_element(locator)
        return self.driver.find_elements(*locator)

    @allure.step("Получить номер последнего заказа из История заказов")
    def get_last_order_history(self):
        return self.find_all_elements(OrderLocators.NUMBERS_HISTORY_ORDER)[-1].text

    @allure.step("Получение номера заказа из попапа")
    def get_order_number_from_popup(self):
        order_number_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,'//h2[contains(@class, "Modal_modal__title__") and contains(@class, "text_type_digits-large")]')))
        return order_number_element.text

    @allure.step("Поиск заказа в истории по номеру")
    def find_order_in_history(self, order_number):
        wait = WebDriverWait(self.driver, 10)
        orders = self.driver.find_elements(*OrderLocators.NUMBERS_ORDER)
        while orders:
            for order in orders:
                if order.text == order_number:
                    return True
            self.driver.execute_script("arguments[0].scrollIntoView();", orders[-1])

            wait.until(EC.presence_of_element_located(OrderLocators.NUMBERS_ORDER))
            orders = self.driver.find_elements(*OrderLocators.NUMBERS_ORDER)
        return False

    @allure.step("Прокрутка до попапа с номером заказа")
    def scroll_to_order_number_popup(self, order_number_popup_locator):
        order_number_element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(order_number_popup_locator))
        actions = ActionChains(self.driver)
        actions.move_to_element(order_number_element).perform()

        WebDriverWait(self.driver, 5).until(EC.visibility_of(order_number_element))
        if order_number_element.is_displayed():
            print("Элемент стал видимым!")
        else:
            print("Не удалось сделать элемент видимым!")

    @allure.step("Получение элемента с номером заказа")
    def get_check_number_order(self, last_order):
        return self.find_clickable_element((By.XPATH,f'//*[contains(@class,"rderHistory_textBox__")]//*[contains(@class,"text_type_digits-default") and contains(text(),"{last_order}")]'))


    @allure.step('Возвращает список номеров заказов или пустой список, если все заказы выполнены')
    def get_orders_in_progress(self):
        WebDriverWait(self.driver, 20).until(
            lambda d: d.find_elements(*OrderLocators.ORDER_IN_PROGRESS) or
                      d.find_elements(*OrderLocators.SEARCH_ORDERS_IN_WORK_DONE),
            message="Не появились ни заказы в работе, ни сообщение о готовности всех заказов."
        )
        orders_in_progress = self.get_elements(OrderLocators.ORDER_IN_PROGRESS)

        if orders_in_progress:
            return [order.text.strip() for order in orders_in_progress if order.text.strip().isdigit()]
        return []





