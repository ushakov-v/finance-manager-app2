import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUI:
    @pytest.fixture(scope="class")
    def setup(self):
        """Настройка браузера перед тестами"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()  # Открыть браузер на полный экран
        self.driver.get("http://localhost:8000")  # Убедитесь, что ваше приложение работает на localhost

        # Ожидание, пока элемент для ввода имени пользователя станет доступным
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        # Вход в систему для тестов (при необходимости)
        self.login()

        yield self.driver  # Позволяет использовать self.driver в тестах после выполнения setup

        # Очистка после теста
        self.driver.quit()

    def login(self):
        """Функция для выполнения входа"""
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        username.send_keys("newuser")
        password.send_keys("password_123!")
        login_button.click()

    # def test_login_page_elements(self, setup):
    #     """Проверка наличия всех элементов на странице входа"""
    #     driver = setup  # Используем драйвер из фикстуры setup
    #     assert "Вход" in driver.title  # Проверка заголовка страницы
    #
    #     # Проверка наличия полей и кнопки
    #     assert driver.find_element(By.NAME, "username")
    #     assert driver.find_element(By.NAME, "password")
    #     assert driver.find_element(By.XPATH, "//button[@type='submit']")
    #
    # def test_registration_form(self, setup):
    #     """Проверка формы регистрации"""
    #     driver = setup  # Используем driver из фикстуры setup
    #     driver.get("http://localhost:8000/register/")  # Переходим на страницу регистрации
    #
    #     # Проверка наличия всех элементов формы регистрации
    #     assert driver.find_element(By.NAME, "username")
    #     assert driver.find_element(By.NAME, "email")
    #     assert driver.find_element(By.NAME, "password1")
    #     assert driver.find_element(By.NAME, "password2")
    #     assert driver.find_element(By.XPATH, "//button[@type='submit']")
    #
    #     # Заполнение формы некорректными данными
    #     username = driver.find_element(By.NAME, "username")
    #     email = driver.find_element(By.NAME, "email")
    #     password1 = driver.find_element(By.NAME, "password1")
    #     password2 = driver.find_element(By.NAME, "password2")
    #     username.send_keys("newuser")
    #     email.send_keys("newuser@example.com")
    #     password1.send_keys("password_123!")
    #     password2.send_keys("password_123!")
    #     driver.find_element(By.XPATH, "//button[@type='submit']").click()
    #
    #     time.sleep(2)  # Ждем, пока произойдет отправка формы (можно заменить на явное ожидание)

    # def test_transaction_list_page(self, setup):
    #     """Проверка страницы с транзакциями"""
    #     driver = setup  # Используем driver из фикстуры setup
    #     driver.get("http://localhost:8000/transactions/")  # Переходим на страницу с транзакциями
    #
    #     # Ожидание, пока таблица с транзакциями станет доступной
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "transaction-table"))
    #     )
    #
    #     # Проверка наличия таблицы с транзакциями
    #     assert driver.find_element(By.CLASS_NAME, "transaction-table")
    #
    #     # Проверка наличия заголовков в таблице
    #     assert driver.find_element(By.TAG_NAME, "th")  # Проверка, что в таблице есть хотя бы один заголовок
    #
    #     # Проверка наличия фильтров
    #     assert driver.find_element(By.XPATH, "//a[contains(text(), 'Все')]")
    #     assert driver.find_element(By.XPATH, "//a[contains(text(), 'Доходы')]")
    #     assert driver.find_element(By.XPATH, "//a[contains(text(), 'Расходы')]")

    # def test_add_transaction(self, setup):
    #     """Проверка добавления транзакции"""
    #     driver = setup  # Используем driver из фикстуры setup
    #     driver.get("http://localhost:8000/add/")  # Переходим на страницу добавления транзакции
    #
    #     # Ожидаем, что элементы формы для добавления транзакции станут доступными
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "transaction_type"))
    #     )
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "amount"))
    #     )
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "date"))
    #     )
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "description"))
    #     )
    #
    #     # Проверка наличия полей для ввода данных
    #     assert driver.find_element(By.NAME, "transaction_type")
    #     assert driver.find_element(By.NAME, "amount")
    #     assert driver.find_element(By.NAME, "date")
    #     assert driver.find_element(By.NAME, "description")
    #
    #     # Заполнение формы добавления транзакции
    #     transaction_type = driver.find_element(By.NAME, "transaction_type")
    #     amount = driver.find_element(By.NAME, "amount")
    #     date = driver.find_element(By.NAME, "date")
    #     description = driver.find_element(By.NAME, "description")
    #
    #     transaction_type.send_keys("income")
    #     amount.send_keys("500")
    #     date.send_keys("01-12-2024")
    #     description.send_keys("Test income transaction")
    #
    #     driver.find_element(By.XPATH, "//button[@type='submit']").click()
    #
    #     # Ожидаем, что новая транзакция появится на странице (например, проверяем текст)
    #     WebDriverWait(driver, 2).until(
    #         EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Test income transaction")
    #     )
    #
    # def test_edit_transaction(self, setup):
    #     """Проверка редактирования транзакции"""
    #     driver = setup  # Используем driver из фикстуры setup
    #     driver.get("http://localhost:8000/transactions/")  # Переходим на страницу транзакций
    #
    #     # Ожидаем, что кнопки редактирования будут доступны
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Редактировать')]"))
    #     )
    #
    #     # Найти кнопку редактирования для первой транзакции и кликнуть по ней
    #     edit_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Редактировать')]")
    #     edit_button.click()
    #
    #     # Ожидаем загрузки страницы редактирования транзакции
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "amount"))
    #     )
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "description"))
    #     )
    #
    #     # Изменение данных транзакции
    #     amount = driver.find_element(By.NAME, "amount")
    #     description = driver.find_element(By.NAME, "description")
    #
    #     amount.clear()
    #     amount.send_keys("1000")
    #     description.clear()
    #     description.send_keys("Updated transaction")
    #
    #     driver.find_element(By.XPATH, "//button[@type='submit']").click()
    #
    #     # Ожидаем, что изменения отразятся на странице транзакций
    #     WebDriverWait(driver, 10).until(
    #         EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Updated transaction")
    #     )

    # def test_delete_transaction(self, setup):
    #     """Проверка удаления транзакции"""
    #     driver = setup  # Используем driver из фикстуры setup
    #     driver.get("http://localhost:8000/transactions/")  # Переходим на страницу транзакций
    #
    #     # Ожидаем, что кнопки удаления будут доступны
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Удалить')]"))
    #     )
    #
    #     # Найдем кнопку удаления для первой транзакции и кликнем по ней
    #     delete_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Удалить')]")
    #     delete_button.click()
    #
    #     # Ожидаем появления первого алерта и подтверждаем его
    #     WebDriverWait(driver, 10).until(
    #         EC.alert_is_present()  # Ожидаем, что первый алерт появился
    #     )
    #     alert = driver.switch_to.alert
    #     alert.accept()  # Принять первый алерт (подтвердить)
    #
    #     # Ожидаем, что откроется страница с дополнительным подтверждением
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(), 'Удалить')]"))
    #     )
    #
    #     # Находим и нажимаем кнопку для окончательного удаления
    #     confirm_delete_button = driver.find_element(By.XPATH,
    #                                                 "//button[@type='submit' and contains(text(), 'Удалить')]")
    #     confirm_delete_button.click()
    #
    #     # Ожидаем, что транзакция была удалена и проверяем, что на странице больше нет данной транзакции
    #     WebDriverWait(driver, 10).until(
    #         EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(), 'Тестовая транзакция')]"))
    #     )

    def test_filter_transactions(self, setup):
        """Проверка фильтрации транзакций"""
        driver = setup  # Используем driver из фикстуры setup
        driver.get("http://localhost:8000/transactions/")  # Переходим на страницу транзакций

        def apply_filter_and_verify(filter_text, expected_type):
            # Нажимаем на ссылку фильтрации
            filter_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{filter_text}')]"))
            )
            filter_element.click()

            # Ждём, пока таблица обновится
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table"))
            )

            # Попытка найти строку с сообщением об отсутствии транзакций
            try:
                no_transactions_row = driver.find_element(By.XPATH,
                                                          "//table/tbody/tr/td[contains(text(), 'Транзакции отсутствуют.')]")
                # Если найдено сообщение, проверяем его
                assert "Транзакции отсутствуют." in no_transactions_row.text, "Ожидалось сообщение об отсутствии транзакций."
            except NoSuchElementException:
                # Если сообщение не найдено, значит есть транзакции, проверяем их
                # Получаем все строки таблицы в tbody
                data_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

                # Проходим по каждой строке и проверяем первый столбец
                for row in data_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        first_cell_text = cells[0].text.strip()
                        assert expected_type in first_cell_text, f"Ожидался тип '{expected_type}' в строке: {row.text}"

        # Проверка фильтрации по доходам
        apply_filter_and_verify("Доходы", "Доход")

        # Проверка фильтрации по расходам
        apply_filter_and_verify("Расходы", "Расход")


