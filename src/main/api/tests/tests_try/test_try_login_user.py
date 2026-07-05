from src.main.api.models.login_user_request_model import LoginUserRequest
from src.main.api.classes.api_manager import ApiManager
class TestLoginUser:
    def test_try_login_admin(self, api_manager: ApiManager):
        login_admin_request = LoginUserRequest(username="admin", password="123456" )
        login_admin_response = api_manager.admin_steps.login_user(login_admin_request)

        assert login_admin_response.user.username == login_admin_request.username

    def test_try_login_user(self, api_manager: ApiManager, create_user_request):
        create_user_response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == create_user_response.user.username
        assert create_user_response.user.role == "ROLE_USER"