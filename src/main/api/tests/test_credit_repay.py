
class TestCreditRepay:
    def test_credit_repay(self, api_manager, credit_repay_requests):

        credit_history_before_repay_response = api_manager.user_steps.credit_history_request(credit_repay_requests)

        # проверяем что кредитный баланс пополнился
        assert credit_history_before_repay_response.credits[0].balance == -credit_repay_requests["credit_repay_request"].amount

        api_manager.user_steps.credit_repay_request(credit_repay_requests)

        credit_history_after_repay_response = api_manager.user_steps.credit_history_request(credit_repay_requests)

        # проверяем что кредит погашен
        assert credit_history_after_repay_response.credits[0].balance == 0

    def test_invalid_credit_repay(
            self,
            api_manager,
            invalid_credit_repay_requests):

        api_manager.user_steps.invalid_credit_repay_request(
            invalid_credit_repay_requests)  # проверяем что нельзя погасить кредит частями
