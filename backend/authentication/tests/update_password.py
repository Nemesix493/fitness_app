from rest_framework.test import APITestCase


class TestUpdatePassword(APITestCase):
    def test_update_success(self):
        # update password with valid data should return http200
        pass

    def test_update_error(self):
        # update password without get loged should return http401
        # update password with wrong old password should return http403
        # update password with not valid new password should return http400
        pass

    def test_update_non_post_method_error(self):
        # update password on any other HTTP verb should return http405
        pass
