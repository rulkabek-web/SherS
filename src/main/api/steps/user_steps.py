from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.models.create_user_request_model import CreateUserRequest


class UserSteps(BaseSteps):

    def create_account(self, create_user_request: CreateUserRequest):
        create_account_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_created(),
            endpoint=Endpoint.CREATE_ACCOUNT
        ).post()

        # self.created_object.append(create_account_response)

        return create_account_response

    def deposit(self, requests):

        create_user_request = requests["create_user_request"]
        deposit_request = requests["deposit_request"]

        deposit_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.DEPOSIT
        ).post(deposit_request)

        return deposit_response

    def invalid_deposit(self, requests):

        create_user_request = requests.get("create_user_request")
        deposit_request = requests.get("deposit_request")

        deposit_response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_bad(),
            endpoint=Endpoint.DEPOSIT
        ).post(deposit_request)

        return deposit_response

    def transfer(self, requests):
        create_user_request = requests.get("create_user_request")
        transfer_request = requests.get("transfer_request")

        transfer_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.TRANSFER
        ).post(transfer_request)

        return transfer_response

    def transactions(self, requests):
        create_user_request = requests.get("create_user_request")
        user_id = requests.get("id")

        transactions_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.TRANSACTIONS
        ).get(user_id)

        return transactions_response

    def invalid_transfer(self, requests):
        create_user_request = requests.get("create_user_request")
        transfer_request = requests.get("transfer_request")

        transfer_response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_bad(),
            endpoint=Endpoint.TRANSFER
        ).post(transfer_request)

        return transfer_response

    def credit_request(self, requests):
        create_user_request = requests.get("create_user_request")
        credit_request = requests.get("credit_request")

        credit_request_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_created(),
            endpoint=Endpoint.CREDIT_REQUEST
        ).post(credit_request)

        return credit_request_response

    def invalid_credit_request(self, requests):
        create_user_request = requests.get("create_user_request")
        credit_request = requests.get("credit_request")

        credit_request_response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_not_found(),
            endpoint=Endpoint.CREDIT_REQUEST
        ).post(credit_request)

        return credit_request_response

    def credit_repay_request(self, requests):
        create_user_request = requests.get("create_user_request")
        credit_repay_request = requests.get("credit_repay_request")

        credit_repay_request_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.CREDIT_REPAY
        ).post(credit_repay_request)

        return credit_repay_request_response

    def credit_history_request(self, requests):
        create_user_request = requests.get("create_user_request")

        credit_history_request_response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.CREDIT_HISTORY
        ).get()

        return credit_history_request_response

    def invalid_credit_repay_request(self, requests):
        create_user_request = requests.get("create_user_request")
        credit_repay_request = requests.get("credit_repay_request")

        credit_repay_request_response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            response_spec=ResponseSpecs.request_unprocessable_content(),
            endpoint=Endpoint.CREDIT_REPAY
        ).post(credit_repay_request)

        return credit_repay_request_response
