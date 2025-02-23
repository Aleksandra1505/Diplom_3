from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.url import MAIN_PAGE_URL
import allure

class BasePageMetod:
   def __init__(self, driver):
       self.driver = driver

   @allure.step("Открыть Главную страницу")
   def open_main_page(self):
       self.driver.get(MAIN_PAGE_URL)

   @allure.step('Найти элемент на странице и дождаться его загрузки')
   def find_elements_with_wait(self, locator, timeout=10):
       return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator),message=f"Элемент с локатором {locator} не найден на странице")

   @allure.step('Проверить видимость элемента на странице')
   def is_element_visible(self, locator, timeout=10):
       element = self.find_elements_with_wait(locator, timeout)
       return element.is_displayed()

   @allure.step('Проверка, что элемент больше не виден')
   def is_element_not_visible(self, locator):
       element = self.find_elements_with_wait(locator)
       return element and not element.is_displayed()

   @allure.step('Тап по элементу (с использованием JavaScript)')
   def click_to_element(self, locator, timeout=10):
       element = WebDriverWait(self.driver, timeout).until(
           EC.element_to_be_clickable(locator),
           message=f"Элемент с локатором {locator} не кликабелен"
       )
       try:
           element.click()  #пробуем кликнуть "обычным" методом
       except Exception:
           #если обычный клик не работает, используем JavaScript
           self.driver.execute_script("arguments[0].click();", element)

   @allure.step('Получить текст')
   def get_text_from_element(self, locator):
       element = self.find_elements_with_wait(locator)
       return element.text

   @allure.step('Дождаться элемент')
   def wait_for_element(self, locator):
       return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))

   @allure.step('Скролл до элемента')
   def scroll_to_element(self, locator):
       element = self.driver.find_element(*locator)
       self.driver.execute_script('arguments[0].scrollIntoView();', element)

   @allure.step('Получить элемент')
   def get_elements(self, locator):
       elements = self.find_elements_with_wait(locator)
       return elements if isinstance(elements, list) else [elements]

   @allure.step('Ожидает и возвращает видимый элемент')
   def find_visible_element(self, locator, timeout=10):
       return WebDriverWait(self.driver, timeout).until(
           EC.visibility_of_element_located(locator),
           message=f"Видимый элемент с локатором {locator} не найден"
       )

   @allure.step('Получение значения счетчика')
   def get_counter_value(self, locator):
       element = self.find_elements_with_wait(locator)
       text = element.text.strip()

       # Проверяем, является ли текст числом
       if text.isdigit():
           return int(text.replace("#", "").strip())
       else:
           # Возвращаем 0, если текст не является числом (или можно вернуть любое другое значение)
           return 0