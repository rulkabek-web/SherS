from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from sqlalchemy.orm import Session
from src.main.api.models.base_model import BaseModel

class TestCreditRequest:

    def test_credit_request(
            self,
            api_manager: ApiManager,
            credit,
            credit_account_id,
            transfer_requests: dict[str, BaseModel],
            db_session: Session
    ):

        credit_request_response = api_manager.user_steps.credit_request(credit)

        api_manager.user_steps.transfer(transfer_requests)

        transactions_response = api_manager.user_steps.transactions(credit_account_id)
        print("transactions_response: ", transactions_response)

        credit_from_db = Credit.get_credit_by_id(db_session, credit_request_response.creditId)
        #проверяем что кредит есть в бд
        assert credit_from_db.id == credit_request_response.creditId, "кредита нет в бд"

        get_transaction_to_from_account_id = Transaction.get_transactions_to_from_account_id(db_session, transfer_requests["transfer_request"].fromAccountId)
        print("!!!!!!!!!!!!!!",get_transaction_to_from_account_id)
        # проверяем что в бд есть транзакция
        assert get_transaction_to_from_account_id.to_account_id ==  transfer_requests["transfer_request"].toAccountId

        # проверяем что баланс пополнился на сумму кредита
        assert transactions_response.balance == credit["credit_request"].amount



        for t in transactions_response.transactions:
            # находим по id транзакцию на перевод
            if t.toAccountId == transfer_requests.get("transfer_request").toAccountId:
                # проверяем что сумма перевода совпадает
                assert t.amount == -transfer_requests.get("transfer_request").amount

    def test_invalid_credit_request(self, api_manager: ApiManager, credit):
        # проверяем что не можем взять 2 кредит на аккаунт, получаем код 404 вместо 403:Уже есть активный кредит
        api_manager.user_steps.credit_request(credit)
        api_manager.user_steps.invalid_credit_request(credit)
