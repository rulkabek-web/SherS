import allure
from src.main.ui.pages.checkout_page import CheckoutPage
from playwright.sync_api import Page, expect

class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)

    @allure.step("заполняем поля information")
    def fill_information(self,first_name: str, last_name: str, zip_postal_code: str):
        self.checkout.fill_information(first_name, last_name, zip_postal_code)
        return self

    @allure.step("Завершаем checkout")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Получаем текст ошибки")
    def get_error_message(self):
        return self.checkout.get_error_message()

    @allure.step("Получаем текст после выполнения")
    def get_success_message(self):
        return self.checkout.get_success_message()

    @allure.step("получаем итоговую сумму товаров")
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()



