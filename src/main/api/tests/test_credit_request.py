from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import  TransactionCrudDb as Transaction
from typing import Annotated, Any, Callable
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.fixtures.fixtures_models.fixtures_models import AccountData

from sqlalchemy.orm import Session
from src.main.api.models.base_model import BaseModel


class TestCreditRequest:

    def test_credit_request(
            self,
            api_manager: ApiManager,
            credit: dict[str, BaseModel],
            credit_account_id: AccountData,
            transfer_requests_factory: Callable[..., dict[str, Any]],
            db_session: Session,
            another_account_id: AccountData
    ):
        credit_request_response = api_manager.user_steps.credit_request(credit)

        transactions_response = api_manager.user_steps.transactions(credit_account_id)

        # проверяем что баланс пополнился на сумму кредита
        assert transactions_response.balance == credit["credit_request"].amount, "баланс не пополнен"

        requests = transfer_requests_factory(
            from_account=credit_account_id,
            to_account=another_account_id,
            amount=Annotated[float, CreationRule(min_float=1000, max_float=credit["credit_request"].amount)],
            make_deposit=False
        )
        transfer_requests = requests

        api_manager.user_steps.transfer(transfer_requests)

        credit_from_db = Credit.get_credit_by_creditId(db_session, credit_request_response.creditId)
        # проверяем что кредит есть в бд
        assert credit_from_db.id == credit_request_response.creditId, "кредита нет в бд"

        transactions_from_db = Transaction.get_transactions_to_account_id(
            db_session, transfer_requests["transfer_request"].toAccountId
        )
        # проверяем что в бд есть транзакция
        assert transactions_from_db.to_account_id == transfer_requests["transfer_request"].toAccountId, "транзакции нет в бд"

        # проверяем что кредитные деньги переведены на другой аккаунт
        assert transactions_from_db.amount == transfer_requests["transfer_request"].amount, "транзакции нет в бд"

    def test_invalid_credit_request(
            self,
            api_manager: ApiManager,
            credit: dict[str, BaseModel],
            credit_account_id: AccountData,
            transfer_requests_factory: Callable[..., dict[str, Any]],
            db_session: Session,
            another_account_id: AccountData
    ):
        credit_request_response = api_manager.user_steps.credit_request(credit)

        transactions_response = api_manager.user_steps.transactions(credit_account_id)

        # проверяем что баланс аккаунта пополнился на сумму первого кредита
        assert transactions_response.balance == credit["credit_request"].amount, "баланс не пополнен"

        credit_from_db = Credit.get_credit_by_creditId(db_session, credit_request_response.creditId)
        # проверяем что кредит есть в бд
        assert credit_from_db.id == credit_request_response.creditId, "кредита нет в бд"

        get_account_by_id_from_db = Account.get_account_by_id(db_session, credit_request_response.id)
        #проверяем что аккаунт в бд пополнился на сумму первого кредита
        assert get_account_by_id_from_db.balance == credit_request_response.amount, "аккаунт в бд не пополнен"

        # проверяем что не можем взять 2 кредит на аккаунт, получаем код 404 вместо 403:Уже есть активный кредит
        api_manager.user_steps.invalid_credit_request(credit)

        another_transactions_response = api_manager.user_steps.transactions(credit_account_id)

        # проверяем что баланс аккаунта не пополнился после второго кредита
        assert another_transactions_response.balance == credit["credit_request"].amount, "баланс пополнен"

        another_get_account_by_id_from_db = Account.get_account_by_id(db_session, credit_request_response.id)
        #проверяем что аккаунт в бд не пополнился на сумму первого кредита
        assert another_get_account_by_id_from_db.balance == credit_request_response.amount, "аккаунт в бд пополнен"