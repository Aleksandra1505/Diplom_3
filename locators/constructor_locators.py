from selenium.webdriver.common.by import By

class ConstructorLocators:
    CONSTRUCTOR_PAGE = (By.XPATH, '//*[contains(text(),"Конструктор")]') #кнопка конструктор в хэддере
    CONSTRUCTOR_HEADER = (By.XPATH, '//*[contains(text(),"Соберите бургер")]') #заголовок на главной странице
    ORDERS_FEED_HEADER = (By.XPATH, '//*[contains(text(),"Лента Заказов")]') #кнопка лента заказов в хэддере
    LIST_ORDER_FEED = (By.XPATH, '//*[contains(@class,"OrderFeed_list__")]') #список ленты заказов
    INFO_INGREDIENT = (By.XPATH, '//h2[contains(text(),"Детали ингредиента")]') #детали ингредиента
    ELEMENT_INGREDIENT = (By.XPATH, '//*[contains(@class,"BurgerIngredient_ingredient__")]') #счётчик ингредиента
    COUNTER_INGREDIENT = (By.XPATH, '//*[contains(@class,"BurgerIngredient_ingredient__")]//*[contains(@class,"counter_default__")]')
    BUTTON_CLOSE_INFO_INGREDIENT = (By.XPATH, '//button[contains(@class, "Modal_modal__close")]') #кнопка Закрыть
    INGREDIENT_LOCATOR = (By.XPATH,"//a[contains(@class, 'BurgerIngredient_ingredient__1TVf6') and contains(text(), 'Флюоресцентная булка R2-D3')]")# Локатор для ингредиента
    COUNTER_LOCATOR = (By.XPATH, "//div[contains(@class, 'counter_counter__ZNLkj')]//p[contains(@class, 'counter_counter__num__3nue1')]")# Локатор для счетчика (по его классу и тексту)
    ORDER_BUTTON = (By.XPATH, '//button[contains(text(), "Оформить заказ")]') #кнопка Оформить заказ
    ORDER_CONFIRMATION_POPUP = (By.XPATH, '//p[contains(text(), "Ваш заказ начали готовить")]')
    ORDERS_FEED_TOTAL_COMPLETED = (By.XPATH, '//p[contains(@class, "OrderFeed_number__")]')
    ORDER_BLOCK = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list__')]")

