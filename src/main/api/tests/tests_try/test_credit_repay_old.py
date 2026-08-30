from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.base_model import BaseModel
from typing import Annotated, Any, Callable
from src.main.api.db.crud.transaction_crud import  TransactionCrudDb as Transaction
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.fixtures_models.fixtures_models import AccountData
from sqlalchemy.orm import Session


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

        credit_history_before_repay_response = api_manager.user_steps.credit_history_request(credit_repay_requests)

        # проверяем что кредитный баланс пополнился
        assert credit_history_before_repay_response.credits[0].balance == -credit_repay_requests["credit_repay_request"].amount

        api_manager.user_steps.credit_repay_request(credit_repay_requests)

        credit_history_after_repay_response = api_manager.user_steps.credit_history_request(credit_repay_requests)

        # проверяем что кредит погашен
        assert credit_history_after_repay_response.credits[0].balance == 0

    def test_invalid_credit_repay(
            self,
            api_manager: ApiManager,
            invalid_credit_repay_requests):

        api_manager.user_steps.invalid_credit_repay_request(
            invalid_credit_repay_requests)  # проверяем что нельзя погасить кредит частями
