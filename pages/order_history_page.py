from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.profile_locators import ProfileLocators
from locators.constructor_locators import ConstructorLocators
from pages.url import MAIN_PAGE_URL, ORDER_HISTORY_URL, FEED_URL
from selenium.webdriver.common.by import By
from locators.order_locators import OrderLocators
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import allure

class OrderPage(BasePage):
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

    @allure.step('Перейти на страницу Лента заказов')
    def go_to_feed(self, driver):
        self.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))

    @allure.step("Получить номер последнего заказа из История заказов")
    def get_last_order_history(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(OrderLocators.NUMBERS_ORDER))
        return self.find_all_elements(OrderLocators.NUMBERS_HISTORY_ORDER)[-1].text

    @allure.step('Переход по клику на «Конструктор»')
    def go_to_constructor(self):
        self.click_to_element(ConstructorLocators.CONSTRUCTOR_PAGE)

    def go_to_orders_feed_page(self):
        self.driver.find_element(*ConstructorLocators.ORDERS_FEED_HEADER).click()
        WebDriverWait(self.driver, 10).until(EC.url_to_be(FEED_URL))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(OrderLocators.COUNTER_DONE_ALL_TIME)
        )

    @allure.step('Переход в Ленту заказов и проверка номера заказа')
    def go_to_feed_and_check_order_number(self, driver):
        # Переходим в Ленту заказов
        self.click_to_element(ConstructorLocators.ORDERS_FEED_HEADER)

        # Ожидаем загрузки страницы Ленты заказов
        WebDriverWait(driver, 10).until(EC.url_to_be(FEED_URL))

        # Ожидаем, пока элемент с номером заказа станет видимым
        order_number_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(OrderLocators.ORDER_NUMBER_POPUP)
        )

        # Ожидаем, пока номер заказа не будет отличаться от "9999"
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(*OrderLocators.ORDER_NUMBER_POPUP).text != "9999"
        )

        # Получаем номер заказа, приводим его к строке и дополняем до 7 символов
        expected_order_number = order_number_element.text
        expected_order_number = str(expected_order_number).zfill(7)

        # Ожидаем, пока номер заказа появится в ленте заказов
        WebDriverWait(driver, 10).until(
            lambda d: any(expected_order_number in el.text for el in d.find_elements(*OrderLocators.ORDER_IN_PROGRESS))
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
        return WebDriverWait(self.driver, 20).until(
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

    @allure.step("Ожидание появления номера заказа в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, timeout=30):
        formatted_order_number = self.format_order_number(order_number)
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(
                formatted_order_number in el.text for el in d.find_elements(*OrderLocators.ORDER_IN_PROGRESS)),
            message=f"Номер заказа {formatted_order_number} не появился в разделе 'В работе'"
        )

    @allure.step("Получение списка заказов в разделе 'В работе'")
    def get_order_number_from_popup(self):
        order_number_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(OrderLocators.ORDER_NUMBER_POPUP)
        )
        return self.format_order_number(order_number_element.text)  # Теперь возвращает отформатированный номер




