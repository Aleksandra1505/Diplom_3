from selenium.webdriver.common.by import By

class ProfileLocators:
    BUTTON_HEADER_DESIGNER = (By.XPATH, '//*[contains(text(),"Конструктор")]') #кнопка Конструктор
    HEADER_LOGIN = (By.XPATH, '//h2[text()="Вход"]') #заголовок на странице /login
    EMAIL_INPUT = (By.XPATH, '//label[text()="Email"]/following-sibling::input') #поле ввода эмейла
    PASSWORD_INPUT = (By.XPATH, '//label[text()="Пароль"]/following-sibling::input') #поле ввода пароля
    LOGIN_BUTTON = (By.XPATH, '//button[text()="Войти"]') #кнопка войти
    ORDER_HISTORY_BUTTON = (By.XPATH, '//a[text()="История заказов"]')  #раздел История заказов на странице /account/profile
    LOGOUT_BUTTON = (By.XPATH, '//button[text()="Выход"]') #кнопка Выход на странице /account/profile
    BUTTON_PROFILE = (By.XPATH, '//a[@href="/account"]') #кнопка Личный кабинет






