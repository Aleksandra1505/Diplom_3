from selenium.webdriver.common.by import By

class OrderLocators:
    NUMBERS_ORDER = (By.XPATH, '//*[contains(@class,"rderHistory_textBox__")]//*[contains(@class,"text_type_digits-default")]') #номер заказа в ленте
    ORDER_DETAILS_MODAL = (By.XPATH, '//*[contains(@class,"odal_orderBox_")]') #окно информации о заказе
    COUNTER_DONE_ALL_TIME = (By.XPATH, '//*[contains(text(),"Выполнено за все время")]/..//*[contains(@class,"rderFeed_number__")]') #заказы в Выполнено за всё время
    COUNTER_DONE_TODAY = (By.XPATH, '//*[contains(text(),"Выполнено за сегодня")]/..//*[contains(@class,"rderFeed_number__")]') #заказы в Выполнено за сегодня
    ORDER_IN_PROGRESS = (By.XPATH, '//*[contains(@class,"OrderFeed_orderListReady_")]') #заказы в разделе В работе
    NUMBERS_HISTORY_ORDER = (By.XPATH, '//*[contains(@class,"rderHistory_textBox__")]//*[contains(@class,"text_type_digits-default")]')  # Номер созданого заказа в истории и ленте
    SEARCH_ORDERS_IN_WORK_DONE = (By.XPATH, './/li[text()="Все текущие заказы готовы!"]')
    LAST_ORDER = (By.XPATH, '//li[contains(@class, "OrderHistory_listItem__2x95r")][1]')
    ORDER_NUMBER_IN_MODAL = (By.XPATH, '//*[contains(@class, "text_type_digits-default") and contains(text(), "#")]')
    ORDER_NUMBER_POPUP = (By.XPATH, '//h2[contains(@class, "Modal_modal__title__") and contains(@class, "text_type_digits-large")]')
    CLOSE_POPUP_BUTTON = (By.XPATH, '//*[@id="root"]/div/section/div[1]/button')
    NUMBER_POPUP_IN_PROFILE = (By.XPATH, '//*[@id="root"]/div/main/div/div/div/ul/li[35]')






