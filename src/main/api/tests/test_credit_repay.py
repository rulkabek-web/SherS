from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.base_model import BaseModel
from typing import Any, Callable
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction, TransactionCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.fixtures_models.fixtures_models import AccountData
from sqlalchemy.orm import Session
from src.main.api.helpers.find_credit import find_credit
import pytest
pytestmark = pytest.mark.api

class TestCreditRepay:
    def test_credit_repay(
            self,
            api_manager: ApiManager,
            credit_repay_requests: dict[str, BaseModel],
            credit: dict[str, BaseModel],
            credit_account_id: AccountData,
            transfer_requests_factory: Callable[..., dict[str, Any]],
            db_session: Session,
            another_account_id: AccountData
    ):
        get_credit_from_db = Credit.get_credit_by_creditId(db_session, credit_repay_requests["credit_request_response"].creditId)
        #  проверяем что кредитный баланс в дб пополнился
        assert get_credit_from_db.amount == credit_repay_requests["credit_repay_request"].amount, "кредит не добавлен в дб"

        get_account_from_db = Account.get_account_by_id(db_session, credit_repay_requests["credit_request_response"].id)

        # проверяем что баланс аккаунта в дб пополнился на сумму кредита
        assert get_account_from_db.balance == credit_repay_requests["credit_repay_request"].amount, "кредитный баланс в дб не пополнен"

        api_manager.user_steps.credit_repay_request(credit_repay_requests)

        credit_history_after_repay_response = api_manager.user_steps.credit_history_request(credit_repay_requests)

        credit = find_credit(credits=credit_history_after_repay_response.credits, accountId=credit_repay_requests["credit_request_response"].id)

        # проверяем что кредит погашен
        assert credit.balance == 0, "кредит не погашен"

        all_transactions = Transaction.get_all_transactions_to_from_account_id(db_session, credit_repay_requests["credit_request_response"].id)

    def test_invalid_credit_repay(
            self,
            api_manager: ApiManager,
            invalid_credit_repay_requests: dict[str, BaseModel],
            credit: dict[str, BaseModel],
            credit_account_id: AccountData,
            transfer_requests_factory: Callable[..., dict[str, Any]],
            db_session: Session,
            another_account_id: AccountData
    ):
        get_credit_from_db = Credit.get_credit_by_creditId(db_session, invalid_credit_repay_requests["credit_request_response"].creditId)
        #  проверяем что кредитный баланс в дб пополнился
        assert get_credit_from_db.amount == invalid_credit_repay_requests["credit_request_response"].amount, "кредит не добавлен в дб"

        get_account_from_db = Account.get_account_by_id(db_session, invalid_credit_repay_requests["credit_request_response"].id)

        # проверяем что баланс аккаунта в дб пополнился на сумму кредита
        assert get_account_from_db.balance == invalid_credit_repay_requests["credit_request_response"].amount, "кредитный баланс в дб не пополнен"

        #проверяем что не можем погасить кредит частями amount/2
        api_manager.user_steps.invalid_credit_repay_request(invalid_credit_repay_requests)

        credit_history_after_repay_response = api_manager.user_steps.credit_history_request(invalid_credit_repay_requests)

        credit = find_credit(credits=credit_history_after_repay_response.credits, accountId=invalid_credit_repay_requests["credit_request_response"].id)

        # проверяем что кредит погашен
        assert credit.balance == -invalid_credit_repay_requests["credit_request_response"].amount,  "кредит погашен"

        all_transactions = Transaction.get_all_transactions_to_from_account_id(db_session, invalid_credit_repay_requests["credit_request_response"].id)

        # проверяем что транзакции погашения кредита нет в бд
        assert len(all_transactions) == 0, "кредит погашен"