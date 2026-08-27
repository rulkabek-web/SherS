from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.checkot_steps import  CheckoutSteps
import pytest

pytestmark = pytest.mark.ui

def test_add_item_and_check_in_cart(page):
    basket = BasketSteps(page)
    catalog = CatalogSteps(page)

    catalog.login("standard_user", "secret_sauce")

    # Добавляем Sauce Labs Backpack
    catalog.add_to_cart("Sauce Labs Backpack")

    # Переходим в корзину
    basket.open_cart()

    # Проверяем, что товар есть
    basket.expect_item_in_cart("Sauce Labs Backpack")

def test_add_two_item_and_check_in_cart(page):
    basket = BasketSteps(page)
    catalog = CatalogSteps(page)

    catalog.login("standard_user", "secret_sauce")

    # Добавляем fleece-jacket и bolt-t-shirt
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    # Переходим в корзину
    basket.open_cart()

    # Проверяем, что товар есть
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

def test_remove_item_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")

    # Добавляем товар в корзину
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    # Переходим в корзину
    basket.open_cart()

    # Проверяем что товар в корзине
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")

    # Удаляем товар
    basket.remove_item("Sauce Labs Fleece Jacket")

    # Проверяем, что товара больше нет в корзине
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")

def test_remove_two_item_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    
    # Добавляем товар в корзину
    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    # Переходим в корзину
    basket.open_cart()

    # Проверяем что товар в корзине
    basket.expect_item_in_cart("Sauce Labs Backpack")
    basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    # Удаляем товар
    basket.remove_item("Sauce Labs Backpack")
    basket.remove_item("Test.allTheThings() T-Shirt (Red)")

    # Проверяем, что товара больше нет в корзине
    basket.expect_item_not_in_cart("Sauce Labs Backpack")
    basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")

def test_e2e(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)


    catalog.login("standard_user", "secret_sauce")

    # Добавляем товар в корзину
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    # Переходим в корзину
    basket.open_cart()

    # Проверяем что товар в корзине
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    # Считаем сумму корзины перед чекаутом
    basket_total = basket.get_items_total_price()

    # Переходим к Checkout
    basket.checkout()

    # заполняем Information
    checkout.fill_information(
        first_name="ser",
        last_name="her",
        zip_postal_code="31113111"
    )

    # Проверяем сумму на Checkout
    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == basket_total, "Сумма товаров в Checkout не совпадает с корзиной"

    # Жмем Finish
    checkout.finish_checkout()
    
    # Проверяем успех оплаты товара
    assert checkout.get_success_message() == "Thank you for your order!"

def test_checkout_without_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)


    catalog.login("standard_user", "secret_sauce")

    # Переход в корзину
    basket.open_cart()

    items = basket.get_item_names()
    assert len(items) == 0, "Корзина не пуста"

    basket.checkout()
    checkout.fill_information(first_name="NewUser", last_name="Nrk", zip_postal_code="")

    # Проверка ошибки о пустой корзине
    error_text = checkout.get_error_message()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"