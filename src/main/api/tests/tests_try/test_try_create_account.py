from src.main.api.classes.api_manager import ApiManager


class TestCreateAccount:
    def test_try_create_account(self, api_manager: ApiManager, create_user_request):
        create_account_response = api_manager.user_steps.create_account(
            create_user_request)

        assert create_account_response.balance == 0
