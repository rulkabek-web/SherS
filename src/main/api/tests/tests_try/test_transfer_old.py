from src.main.api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.base_model import BaseModel

class TestCreateUser:

    def test_transfer(self, db_session: Session, api_manager: ApiManager, transfer_requests: dict[str, BaseModel | int], account_id):
        transfer_response = api_manager.user_steps.transfer(transfer_requests)
        assert transfer_response.fromAccountIdBalance == 18000 - \
            transfer_requests["transfer_request"].amount

        transactions_response = api_manager.user_steps.transactions(account_id)
        # id счета совпадает
        assert transactions_response.id == account_id.get("id")

        user_from_db = User.get_user_by_username(db_session, transfer_requests["create_user_request"].username)
        print(user_from_db)

        for t in transactions_response.transactions:
            # находим по id транзакцию на перевод
            if t.toAccountId == transfer_requests.get("transfer_request").toAccountId:
                # проверяем что сумма перевода совпадает
                assert t.amount == - transfer_requests.get("transfer_request").amount

    def test_invalid_transfer(self, api_manager: ApiManager, invalid_transfer_requests):
        # проверяем что не можем перевести меньше 500 или больше 10000
        api_manager.user_steps.invalid_transfer(invalid_transfer_requests)
