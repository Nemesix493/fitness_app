from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

UserModel = get_user_model()


class TestManageUser(APITestCase):
    def test_get_user_success(self):
        # Manage user on get by a loged user should return http200 and user data
        pass

    def test_get_user_error(self):
        # Manage user on get by a not loged user should return http401
        pass

    def test_put_user_success(self):
        # Manage user on put by a loged user should return http200 and the updated user data
        pass

    def test_put_user_error(self):
        # Manage user on put by a not loged user should return http401
        # Manage user on put by a loged user with not valid or missing data should return http400
        pass

    def test_patch_user_success(self):
        # Manage user on put by a loged user should return http200 and the updated user data
        pass

    def test_patch_user_error(self):
        # Manage user on put by a not loged user should return http401
        # Manage user on put by a loged user with not valid data should return http400
        pass

    def test_other_method_error(self):
        # Any other HTTP verb should return http405
        pass
