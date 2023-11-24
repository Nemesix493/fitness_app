from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

UserModel = get_user_model()


class TokenlessLoginViewTests(APITestCase):
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

    def test_login_success(self):
        # Success login should return http200
        for login in [self.user_data['username'], self.user_data['email']]:
            response = self.client.post(
                path=reverse_lazy('authentication:tokenless-login'),
                data={
                    'login': login,
                    'password': self.user_data['password']
                }
            )
            self.assertEqual(response.status_code, 200)
            self.client.logout()

    def test_login_error(self):
        # Wrong username, email or password should return http404
        credentials = self.user_data.keys()
        for wrong_credential in credentials:
            if wrong_credential in ['username', 'email']:
                login = self.user_data[wrong_credential] + 'wrong'
                password = self.user_data['password']
            else:
                login = self.user_data['username']
                password = self.user_data['password'] + 'wrong'
            response = self.client.post(
                path=reverse_lazy('authentication:tokenless-login'),
                data={
                    'login': login,
                    'password': password
                }
            )
            self.assertEqual(response.status_code, 404)
        # Missing data should return http400
        response = self.client.post(
            path=reverse_lazy('authentication:tokenless-login')
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_http_verb(self):
        # Any other verb than POST should return http405
        http_verbs = [
            self.client.delete,
            self.client.get,
            self.client.patch,
            self.client.put
        ]
        for http_verb in http_verbs:
            response = http_verb(
                path=reverse_lazy('authentication:tokenless-login')
            )
            self.assertEqual(response.status_code, 405)

    def test_reconnect_error(self):
        # Reconnect without log out should return http400
        self.client.force_login(UserModel.objects.get(username=self.user_data['username']))
        response = self.client.post(
            path=reverse_lazy('authentication:tokenless-login'),
            data={
                'login': self.user_data['username'],
                'password': self.user_data['password']
            }
        )
        self.assertEqual(response.status_code, 400)
