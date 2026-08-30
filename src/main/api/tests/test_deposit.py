from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.base_model import BaseModel
from src.main.api.fixtures.fixtures_models.fixtures_models import AccountData
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

from sqlalchemy.orm import Session
import pytest
pytestmark = pytest.mark.api

class TestDeposit:

    def test_deposit(
            self,
            db_session: Session,
            account_id: AccountData,
            api_manager: ApiManager,
            deposit_requests: dict[str, BaseModel]
    ):
        deposit_response = api_manager.user_steps.deposit(deposit_requests)
        #проверяем что депозит начислен
        assert deposit_requests.get("deposit_request").amount == deposit_response.balance, "депозит не начислен"

        transactions_response = api_manager.user_steps.transactions(account_id)
        #проверяем депозит по id
        assert deposit_requests.get("deposit_request").accountId == transactions_response.id, "депозит не начислен"

        get_account_db = Account.get_account_by_id(db_session, account_id["id"])
        #проверяем что в дб создался аккаунт
        assert get_account_db.id == deposit_requests["deposit_request"].accountId, "аккаунта нет в бд"
        #проверяем баланс аккаунта в бд
        assert get_account_db.balance == deposit_response.balance, "депозит не начислен в бд"

    def test_deposit_invalid(
            self,
            db_session: Session,
            api_manager: ApiManager,
            invalid_deposit_requests: dict[str, BaseModel],
            account_id: AccountData
    ):
        # не можем депозитнуть меньше 1000 или больше 9000
        api_manager.user_steps.invalid_deposit(invalid_deposit_requests)

        transactions_response = api_manager.user_steps.transactions(account_id)
        #проверяем что депозит не начислен
        assert transactions_response.balance == 0, "депозит меньше 1000 или больше 9000 начислен"

        account_from_db = Account.get_account_by_id(db_session, account_id["id"])
        #проверяем что аккаунт создан в бд
        assert account_from_db.id == account_id["id"], "аккаунта нет в бд"
        #проверяем что баланс аккаунта в бд не пополнился
        assert account_from_db.balance == transactions_response.balance


