import abc

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

UserModel = get_user_model()


class BaseAuthenticationTest(APITestCase, abc.ABC):
    paths_name = {}
    user_data = {
        'username': 'user_test',
        'email': 'user_test@exemple.com',
        'password': 'passwordtest'
    }

    def setUp(self) -> None:
        self.user_test = UserModel.objects.create(
            **{
                key: val
                for key, val in self.user_data.items()
                if key != 'password'
            }
        )
        self.user_test.set_password(self.user_data['password'])
        self.user_test.save()
        return super().setUp()

    @classmethod
    def setUpClass(cls) -> None:
        cls.get_path()
        return super().setUpClass()

    @classmethod
    def get_path(cls):
        cls.paths = {
            key: reverse_lazy(val)
            for key, val in cls.paths_name.items()
        }
