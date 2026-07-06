import pytest
from src.main.api.generators.creation_rule import CreationRule
from typing import Annotated, Any, Callable
from src.main.api.fixtures.fixtures_models.fixtures_models import AccountData
from src.main.api.models.base_model import BaseModel
from src.main.api.models.credit_repay_request_model import CreditRepayRequest
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.models.deposit_request_model import DepositRequest
from src.main.api.models.create_user_request_model import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.classes.api_manager import ApiManager

@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)

    return user_request

@pytest.fixture
def create_another_user_request(api_manager: ApiManager):
    another_user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(another_user_request)

    return another_user_request

@pytest.fixture
def account_id(api_manager: ApiManager, create_user_request: dict[str, BaseModel]) -> dict[str, BaseModel ]:
    create_account = api_manager.user_steps.create_account(create_user_request)

    account_id = create_account.id
    response = {"create_user_request": create_user_request, "id": account_id }
    return response

@pytest.fixture
def another_account_id(api_manager: ApiManager, create_user_request: dict[str, BaseModel]):
    create_account = api_manager.user_steps.create_account(create_user_request)

    account_id = create_account.id
    response = {"create_user_request": create_user_request, "id": account_id }
    return response

@pytest.fixture
def deposit_requests(api_manager: ApiManager, account_id: AccountData) -> dict[str, BaseModel]:
    deposit_request = RandomModelGenerator.generate(
        DepositRequest,
        accountId=account_id["id"],
        amount=Annotated[float, CreationRule(min_float=1000, max_float=9000)]
    )

    create_user_request = account_id["create_user_request"]

    requests = {"create_user_request": create_user_request, "deposit_request": deposit_request}

    return requests

@pytest.fixture
def invalid_account_id(
        api_manager: ApiManager,
        create_user_request: dict[str, BaseModel],
        create_another_user_request: dict[str, BaseModel]
) -> dict[str, BaseModel]:
    account_id = api_manager.user_steps.create_account(create_user_request).id
    response = {"create_user_request": create_another_user_request, "id": account_id }

    return response

@pytest.fixture(params=
                [
                 Annotated[float,CreationRule(min_float=1, max_float=1000)],
                 Annotated[float,CreationRule(min_float=9000, max_float=18000)]]
                )
def invalid_deposit_requests(request, api_manager: ApiManager, account_id: AccountData) -> dict[str, BaseModel]:
    deposit_request = RandomModelGenerator.generate(
        DepositRequest,
        accountId=account_id["id"],
        amount=request.param
    )

    create_user_request = account_id["create_user_request"]

    requests = {"create_user_request": create_user_request, "deposit_request": deposit_request}

    return requests

@pytest.fixture
def transfer_requests_factory(api_manager: ApiManager) -> Callable[..., dict[str, Any]]:

    def create_transfer_requests(
            from_account: dict[str, BaseModel],
            to_account: dict[str, BaseModel],
            amount: float | None = None,
            make_deposit: bool = True
    )-> dict[str, Any]:

        account_id = from_account
        another_account_id  = to_account

        create_user_request = account_id.get("create_user_request")
        create_another_user_request = another_account_id.get("create_user_request")

        if amount is not None:
            transfer_request = RandomModelGenerator.generate(
                TransferRequest,
                fromAccountId=account_id.get("id"),
                toAccountId=another_account_id.get("id"),
                amount=amount
            )
        else:
            transfer_request = RandomModelGenerator.generate(
                TransferRequest,
                fromAccountId=account_id.get("id"),
                toAccountId=another_account_id.get("id")
            )

        if make_deposit:
            deposit_requests = {}
            deposit_requests["create_user_request"] = create_user_request

            deposit_request_before_transfer = RandomModelGenerator.generate(
                DepositRequest,
                accountId=account_id.get("id"),
                amount=transfer_request.amount
            )
            deposit_requests["deposit_request"] = deposit_request_before_transfer

            api_manager.user_steps.deposit(deposit_requests)

        return {
            "create_user_request": create_user_request,
            "create_another_user_request": create_another_user_request,
            "transfer_request": transfer_request
        }
    return create_transfer_requests

@pytest.fixture(params=[
                        Annotated[float,CreationRule(min_float=1, max_float=499)],
                        Annotated[float,CreationRule(min_float=10001, max_float=18000)]
                        ]
                )
def invalid_transfer_requests(
        api_manager: ApiManager,
        deposit_requests: dict[str, BaseModel],
        account_id: AccountData,
        another_account_id: AccountData,
        request
) -> dict[str, BaseModel]:


    transfer_request = RandomModelGenerator.generate(
        TransferRequest,
        fromAccountId=account_id.get("id"),
        toAccountId=another_account_id.get("id"),
        amount=request.param
    )

    deposit_request_before_transfer = RandomModelGenerator.generate(
        DepositRequest,
        accountId=account_id.get("id"),
        amount=9000
    )
    deposit_requests["deposit_request"] = deposit_request_before_transfer

    api_manager.user_steps.deposit(deposit_requests)
    api_manager.user_steps.deposit(deposit_requests)


    create_user_request = account_id.get("create_user_request")

    requests = {"create_user_request": create_user_request, "transfer_request": transfer_request}

    return requests

@pytest.fixture
def create_credit_user_request(api_manager: ApiManager)-> BaseModel:
    credit_user_request = RandomModelGenerator.generate(
        CreateUserRequest,
        role="ROLE_CREDIT_SECRET"
    )
    api_manager.admin_steps.create_user(credit_user_request)

    return credit_user_request

@pytest.fixture
def credit_account_id(api_manager: ApiManager, create_credit_user_request: BaseModel) -> AccountData:
    create_account = api_manager.user_steps.create_account(create_credit_user_request)

    account_id = create_account.id

    response:AccountData = {"create_user_request": create_credit_user_request, "id": account_id }

    return response

@pytest.fixture
def credit(api_manager: ApiManager, credit_account_id: AccountData) -> dict[str, BaseModel]:
    credit_request = RandomModelGenerator.generate(
        CreditRequest,
        accountId=credit_account_id.get("id"),
        amount=Annotated[int,CreationRule(min_int=5000, max_int=15000)],
        termMonths=Annotated[int,CreationRule(min_int=1, max_int=12)]

    )

    create_user_request = credit_account_id.get("create_user_request")

    requests = {"create_user_request": create_user_request, "credit_request": credit_request}

    return requests

@pytest.fixture
def credit_repay_requests(api_manager: ApiManager, credit):
    credit_request_response = api_manager.user_steps.credit_request(credit)

    credit_repay_request = CreditRepayRequest(
        accountId=credit["credit_request"].accountId,
        amount=credit["credit_request"].amount,
        creditId=credit_request_response.creditId

    )

    create_user_request = credit.get("create_user_request")

    requests = {"create_user_request": create_user_request, "credit_repay_request": credit_repay_request, "credit_request_response": credit_request_response}

    return requests

@pytest.fixture
def invalid_credit_repay_requests(api_manager: ApiManager, credit):
    credit_request_response = api_manager.user_steps.credit_request(credit)

    credit_repay_request = CreditRepayRequest(
        accountId=credit["credit_request"].accountId,
        amount=round((credit["credit_request"].amount)/2), #проверяем что нельзя погасить кредит частями
        creditId=credit_request_response.creditId

    )

    create_user_request = credit.get("create_user_request")

    requests = {"create_user_request": create_user_request, "credit_repay_request": credit_repay_request, "credit_request_response": credit_request_response}

    return requests