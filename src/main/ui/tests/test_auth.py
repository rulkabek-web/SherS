from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.utils.constants import Urls

def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    # Проверяем, что мы на странице каталога после успешного логина
    catalog_page = CatalogSteps(page)
    assert catalog_page.get_products_count() > 0, "Ожидаем товары на странице каталога"


def test_login_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    # Получаем текст ошибки и assert в тесте
    error_text = steps.login_page.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"


    catalog.logout()
    assert page.url == Urls.BASE, "Ожидаем возврат на страницу логина"


def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == Urls.BASE, "Ожидаем возврат на страницу логина"
