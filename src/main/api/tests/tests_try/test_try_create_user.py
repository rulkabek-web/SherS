import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request_model import CreateUserRequest

class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_try_create_user(self, api_manager: ApiManager,create_user_request):

        create_user_response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_response.username == create_user_request.username

    def test_try_create_user_invalid(self, api_manager: ApiManager):
        create_user_request = CreateUserRequest(
            username="G2",
            password="Pas!sw0rd",
            role="ROLE_USER"
        )
        create_user_response = api_manager.admin_steps.create_invalid_user(create_user_request)