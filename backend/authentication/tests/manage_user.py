from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

UserModel = get_user_model()


class TestManageUser(APITestCase):
    user_data = {
        'username': 'user_test',
        'email': 'user_test@exemple.com',
        'password': 'passwordtest'
    }

    def setUp(self) -> None:
        user_test = UserModel.objects.create(
            **{
                key: val
                for key, val in self.user_data.items()
                if key != 'password'
            }
        )
        user_test.set_password(self.user_data['password'])
        user_test.save()
        return super().setUp()

    def test_get_user_success(self):
        # Manage user on get by a loged user should return http200 and user data
        user_test = UserModel.objects.get(username=self.user_data['username'])
        self.client.force_login(user_test)
        response = self.client.get(reverse_lazy('authentication:manage-user'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_error(self):
        # Manage user on get by a not loged user should return http401
        response = self.client.get(reverse_lazy('authentication:manage-user'))
        self.assertEqual(response.status_code, 401)

    def test_put_user_success(self):
        # Manage user on put by a loged user should return http200 and the updated user data
        user_test = UserModel.objects.get(username=self.user_data['username'])
        self.client.force_login(user_test)
        response = self.client.put(
            path=reverse_lazy('authentication:manage-user'),
            data={
                'username': 'new' + user_test.username,
                'id': user_test.id,
                'first_name': '',
                'last_name': ''
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_put_user_error(self):
        # Manage user on put by a not loged user should return http401
        user_test = UserModel.objects.get(username=self.user_data['username'])
        response = self.client.put(
            path=reverse_lazy('authentication:manage-user'),
            data={
                'username': 'new' + user_test.username,
                'id': user_test.id,
                'first_name': '',
                'last_name': ''
            }
        )
        self.assertEqual(response.status_code, 401)
        # Manage user on put by a loged user with not valid or missing data should return http400
        self.client.force_login(user_test)
        response = self.client.put(
            path=reverse_lazy('authentication:manage-user'),
            data={
                'username': '',
                'id': user_test.id,
                'first_name': '',
                'last_name': ''
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_user_success(self):
        # Manage user on put by a loged user should return http200 and the updated user data
        user_test = UserModel.objects.get(username=self.user_data['username'])
        self.client.force_login(user_test)
        response = self.client.put(
            path=reverse_lazy('authentication:manage-user'),
            data={
                'username': 'new' + user_test.username
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_user_error(self):
        # Manage user on put by a not loged user should return http401
        user_test = UserModel.objects.get(username=self.user_data['username'])
        response = self.client.put(
            path=reverse_lazy('authentication:manage-user'),
            data={
                'username': 'new' + user_test.username
            }
        )
        self.assertEqual(response.status_code, 401)
        # Manage user on put by a loged user with not valid data should return http400
        self.client.force_login(user_test)
        response = self.client.put(
            path=reverse_lazy('authentication:manage-user'),
            data={
                'username': ''
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_other_method_error(self):
        # Any other HTTP verb should return http405
        user_test = UserModel.objects.get(username=self.user_data['username'])
        self.client.force_login(user_test)
        response = self.client.delete(
            path=reverse_lazy('authentication:manage-user')
        )
        self.assertEqual(response.status_code, 405)
