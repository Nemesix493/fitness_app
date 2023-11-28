from .base_authentication import BaseAuthenticationTest


class TokenlessLoginViewTests(BaseAuthenticationTest):
    paths_name = {
        'tokenless_login': 'authentication:tokenless-login'
    }

    def test_login_success(self):
        # Success login should return http200
        for login in [self.user_data['username'], self.user_data['email']]:
            response = self.client.post(
                path=self.paths['tokenless_login'],
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
                path=self.paths['tokenless_login'],
                data={
                    'login': login,
                    'password': password
                }
            )
            self.assertEqual(response.status_code, 404)
        # Missing data should return http400
        response = self.client.post(
            path=self.paths['tokenless_login']
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
                path=self.paths['tokenless_login']
            )
            self.assertEqual(response.status_code, 405)

    def test_reconnect_error(self):
        # Reconnect without log out should return http400
        self.client.force_login(self.user_test)
        response = self.client.post(
            path=self.paths['tokenless_login'],
            data={
                'login': self.user_data['username'],
                'password': self.user_data['password']
            }
        )
        self.assertEqual(response.status_code, 400)
