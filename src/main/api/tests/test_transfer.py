from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.base_model import BaseModel
from typing import Annotated, Any, Callable
from src.main.api.fixtures.fixtures_models.fixtures_models import AccountData
from src.main.api.generators.creation_rule import CreationRule
import pytest
pytestmark = pytest.mark.api

class TestTransfer:

    def test_transfer(
            self,
            db_session: Session,
            api_manager: ApiManager,
            deposit_requests: dict[str, BaseModel],
            account_id: AccountData,
            another_account_id: AccountData,
            transfer_requests_factory: Callable[..., dict[str, Any]]
    ):

        requests = transfer_requests_factory(
            from_account=account_id,
            to_account=another_account_id,
            amount = Annotated[float, CreationRule(min_float=1000, max_float=9000)]
        )
        transfer_requests = requests

        api_manager.user_steps.transfer(transfer_requests)

        transactions_response = api_manager.user_steps.transactions(account_id)
        # id счета совпадает
        assert transactions_response.id == account_id.get("id"), "id не найден"

        user_from_db = User.get_user_by_username(
            db_session, transfer_requests["create_user_request"].username)
        # проверяем что в дб создался юзер
        assert user_from_db.username == transfer_requests[
            "create_user_request"].username, "юзера нет в бд"

        get_transaction_to_from_account_id = Transaction.get_transactions_to_from_account_id(
            db_session, transfer_requests["transfer_request"].fromAccountId)
        # проверяем что перевод добавился в бд
        assert get_transaction_to_from_account_id.amount == transfer_requests[
            "transfer_request"].amount, "перевода нет в бд"

        another_transactions_response = api_manager.user_steps.transactions(
            another_account_id)
        # проверяем что второй аккаунт пополнился на сумму перевода
        assert another_transactions_response.balance == transfer_requests.get(
            "transfer_request").amount, "баланс не пополнился"

    def test_invalid_transfer(
            self,
            db_session: Session,
            api_manager: ApiManager,
            invalid_transfer_requests: dict[str, BaseModel],
            another_account_id: AccountData
    ):
        # проверяем что не можем перевести меньше 500 или больше 10000
        api_manager.user_steps.invalid_transfer(invalid_transfer_requests)

        transactions_response = api_manager.user_steps.transactions(
            another_account_id)
        # проверяем что перевод не выполнен
        assert transactions_response.balance == 0, "перевод меньше 500 или больше 10000 выполнен"

        account_from_db = Account.get_account_by_id(
            db_session, another_account_id["id"])
        # проверяем что в дб создался аккаунт
        assert account_from_db.id == another_account_id["id"], "аккаунта нет в бд"
        # проверяем что баланс аккаунта 0
        assert account_from_db.balance == 0, "перевод на аккаунт в бд выполнен "
