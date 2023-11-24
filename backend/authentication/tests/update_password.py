from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

UserModel = get_user_model()


class TestUpdatePassword(APITestCase):
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

    def test_update_success(self):
        # update password with valid data should return http200
        user_test = UserModel.objects.get(username=self.user_data['username'])
        self.client.force_login(user_test)
        response = self.client.post(
            path=reverse_lazy('authentication:update-password'),
            data={
                'old_password': self.user_data['password'],
                'new_password': self.user_data['password'] + '56new'
            }
        )
        self.assertEqual(response.status_code, 200)
        user_test.refresh_from_db()
        self.assertTrue(user_test.check_password(self.user_data['password'] + '56new'))

    def test_update_error(self):
        user_test = UserModel.objects.get(username=self.user_data['username'])
        # update password without get loged should return http401
        response = self.client.post(
            path=reverse_lazy('authentication:update-password'),
            data={
                'old_password': self.user_data['password'],
                'new_password': self.user_data['password'] + '56new'
            }
        )
        self.assertEqual(response.status_code, 401)
        # update password with wrong old password should return http403
        self.client.force_login(user_test)
        response = self.client.post(
            path=reverse_lazy('authentication:update-password'),
            data={
                'old_password': self.user_data['password'] + 'wrong',
                'new_password': self.user_data['password'] + '56new'
            }
        )
        self.assertEqual(response.status_code, 403)
        # update password with not valid new password should return http400
        response = self.client.post(
            path=reverse_lazy('authentication:update-password'),
            data={
                'old_password': self.user_data['password'],
                'new_password': self.user_data['username']
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_update_non_post_method_error(self):
        # update password on any other HTTP verb should return http405
        http_verbs = [
            self.client.delete,
            self.client.get,
            self.client.patch,
            self.client.put
        ]
        user_test = UserModel.objects.get(username=self.user_data['username'])
        self.client.force_login(user_test)
        for http_verb in http_verbs:
            response = http_verb(
                path=reverse_lazy('authentication:update-password')
            )
            self.assertEqual(response.status_code, 405)
