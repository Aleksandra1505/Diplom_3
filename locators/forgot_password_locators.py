from selenium.webdriver.common.by import By

class ForgotPasswordLocators:
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[@href='/forgot-password']") #ссылка восстановить пароль на странице /login
    PASSWORD_RECOVERY_HEADER = (By.XPATH, "//h2[text()='Восстановление пароля']") #заголовок на странице /forgot-password
    RECOVER_BUTTON = (By.XPATH, "//button[text()='Восстановить']") #кнопка Восстановить на странице /forgot-password
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']") #поле ввода эмейла на странице /forgot-password

    PASSWORD_LABEL = (By.XPATH, '//*[contains(text(),"Пароль")]/parent::*/input') #поле ввода пароля на странице /login
    SHOW_PASSWORD = (By.CLASS_NAME, 'input__icon-action') #кнопка показать пароль на странице /reset-password
    TEXT_INPUT = (By.XPATH, "//label[text()='Введите код из письма']") #поле повторного ввода пароля на странице /reset-password
    SAVE_BUTTON = (By.XPATH, "//button[text()='Сохранить']") #кнопка Сохранить на странице /reset-password
    PASSWORD_INPUT_ACTIVE = (By.XPATH, "//input[@name='Пароль' and contains(@class, 'input_status_active')]") #подсветка поля пароль при нажатии на кнопку показа
