from playwright.sync_api import Page, expect


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.get_by_placeholder("First Name")
        self.last_name = page.get_by_placeholder("Last Name")
        self.zip_postal_code = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.locator('[data-test="continue"]')
        self.item_total = page.locator('.summary_subtotal_label')
        self.finish = page.locator('[data-test="finish"]')
        self.error_message = page.locator('[data-test="error"]')
        self.success_message = page.locator(".complete-header")

    def fill_information(self,first_name: str, last_name: str, zip_postal_code: str):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.zip_postal_code.fill(zip_postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish.click()

    def get_error_message(self):
        return self.error_message.inner_text()

    def get_success_message(self):
        return self.success_message.inner_text()

    def get_item_total_after_continue(self) -> float:
        # ждем появления элемента
        expect(self.item_total).to_be_visible()
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))