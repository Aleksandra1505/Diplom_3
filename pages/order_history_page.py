from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.profile_locators import ProfileLocators
from locators.constructor_locators import ConstructorLocators
from pages.url import MAIN_PAGE_URL, ORDER_HISTORY_URL, FEED_URL
from selenium.webdriver.common.by import By
from locators.order_locators import OrderLocators
from selenium.common.exceptions import TimeoutException
import allure

class OrderPage(BasePage):

    @allure.step('Получить кликабельный элемент')
    def find_clickable_element(self, locator):
        WebDriverWait(self.driver, 200).until(lambda driver: driver.find_element(*locator).is_displayed())
        return self.driver.find_element(*locator)

    @allure.step('Получить кликабельный элемент')
    def find_all_elements(self, locator):
        self.find_clickable_element(locator)
        return self.driver.find_elements(*locator)

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

    @allure.step("Получение элемента с номером заказа")
    def get_check_number_order(self, last_order):
        return self.find_clickable_element((By.XPATH,f'//*[contains(@class,"rderHistory_textBox__")]//*[contains(@class,"text_type_digits-default") and contains(text(),"{last_order}")]'))

    """Ниже собраны новые методы, созданные в рамках доработок"""

    @allure.step('Переходим в раздел История заказов')
    def click_to_order_history(self):
        # Кликаем по кнопке "История заказов"
        self.click_to_element(ProfileLocators.ORDER_HISTORY_BUTTON)
        # Ожидаем, что URL изменится на нужный
        WebDriverWait(self.driver, 20).until(EC.url_to_be(ORDER_HISTORY_URL))

    @allure.step('Клик по последнему заказу в списке')
    def click_to_last_order(self):
        # Кликаем по последнему заказу
        self.click_to_element(OrderLocators.LAST_ORDER)
        # Ожидаем появления модального окна с деталями заказа
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(OrderLocators.ORDER_DETAILS_MODAL))

    @allure.step('Возвращает номер заказа из модалки')
    def get_text_from_order_number(self):
        # Получаем текст номера заказа из модального окна
        return self.get_text_from_element(OrderLocators.ORDER_NUMBER_IN_MODAL)

    @allure.step('Закрываем попап заказа')
    def close_popup_order(self):
        self.click_to_element(OrderLocators.CLOSE_POPUP_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

    @allure.step("Получить номер последнего заказа из История заказов")
    def get_last_order_history(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(OrderLocators.NUMBERS_ORDER))
        return self.find_all_elements(OrderLocators.NUMBERS_HISTORY_ORDER)[-1].text

    @allure.step('Переход в Ленту заказов')
    def go_to_orders_feed_page(self):
        self.driver.find_element(*ConstructorLocators.ORDERS_FEED_HEADER).click()
        WebDriverWait(self.driver, 10).until(EC.url_to_be(FEED_URL))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(OrderLocators.COUNTER_DONE_ALL_TIME)
        )

    @allure.step("Получение номера заказа из попапа")
    def get_order_number_from_popup(self):
        order_number_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//h2[contains(@class, "Modal_modal__title__") and contains(@class, "text_type_digits-large")]')))
        return order_number_element.text  # Здесь возвращаем только текст

    @allure.step("Переходит на страницу с лентой заказов и ожидает загрузки URL")
    def navigate_to_order_feed(self):
        print("Переходим в раздел 'В работе'...")

        self.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)

        try:
            WebDriverWait(self.driver, 30).until(EC.url_to_be(FEED_URL))
            print(f"Успешно перешли на страницу 'В работе'. Текущий URL: {self.driver.current_url}")
        except TimeoutException:
            print(f"Ошибка: Не удалось загрузить страницу 'В работе' за 20 секунд.")
            raise  # Пробрасываем исключение дальше

    @allure.step("Ожидает появления номера заказа в попапе")
    def wait_for_order_number_popup(self):
        return WebDriverWait(self.driver, 25).until(
            EC.visibility_of_element_located(OrderLocators.ORDER_NUMBER_POPUP)
        )

    @allure.step("Ожидает, пока номер заказа обновится с дефолтного значения '9999'.")
    def wait_for_order_number_update(self, timeout=40, poll_frequency=1):
        WebDriverWait(self.driver, timeout, poll_frequency).until(
            lambda d: (order_number := d.find_element(
                *OrderLocators.ORDER_NUMBER_POPUP).text) != "9999" and order_number.strip() != "",
            message="Номер заказа не обновился или не появился в попапе"
        )

    @allure.step("Форматирование номера заказа")
    def format_order_number(self, order_number):
        return str(order_number).zfill(7)

    @allure.step("Сохранение номера заказа")
    def set_expected_order_number(self):
        order_number = self.get_order_number_from_popup()
        self.expected_order_number = self.format_order_number(order_number)

    @allure.step("Ожидание появления номера заказа в разделе 'В работе'")
    def wait_for_order_in_progress(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(
                self.expected_order_number in el.text for el in d.find_elements(*OrderLocators.ORDER_IN_PROGRESS)
            ),
            message=f"Номер заказа {self.expected_order_number} не появился в разделе 'В работе'"
        )

    @allure.step("Получение списка заказов в разделе 'В работе'")
    def get_order_number_from_popup(self):
        order_number_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(OrderLocators.ORDER_NUMBER_POPUP)
        )
        return self.format_order_number(order_number_element.text)  # Теперь возвращает отформатированный номер




