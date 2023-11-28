from .base_authentication import BaseAuthenticationTest


class TestManageUser(BaseAuthenticationTest):
    paths_name = {
        'manage_self_user': 'authentication:self:manage-user'
    }

    def test_get_user_success(self):
        # Manage user on get by a loged user should return http200 and user data
        self.client.force_login(self.user_test)
        response = self.client.get(self.paths['manage_self_user'])
        self.assertEqual(response.status_code, 200)

    def test_get_user_error(self):
        # Manage user on get by a not loged user should return http401
        response = self.client.get(self.paths['manage_self_user'])
        self.assertEqual(response.status_code, 401)

    def test_put_user_success(self):
        # Manage user on put by a loged user should return http200 and the updated user data
        self.client.force_login(self.user_test)
        response = self.client.put(
            path=self.paths['manage_self_user'],
            data={
                'username': 'new' + self.user_test.username,
                'id': self.user_test.id,
                'first_name': '',
                'last_name': ''
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_put_user_error(self):
        # Manage user on put by a not loged user should return http401
        response = self.client.put(
            path=self.paths['manage_self_user'],
            data={
                'username': 'new' + self.user_test.username,
                'id': self.user_test.id,
                'first_name': '',
                'last_name': ''
            }
        )
        self.assertEqual(response.status_code, 401)
        # Manage user on put by a loged user with not valid or missing data should return http400
        self.client.force_login(self.user_test)
        response = self.client.put(
            path=self.paths['manage_self_user'],
            data={
                'username': '',
                'id': self.user_test.id,
                'first_name': '',
                'last_name': ''
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_user_success(self):
        # Manage user on put by a loged user should return http200 and the updated user data
        self.client.force_login(self.user_test)
        response = self.client.put(
            path=self.paths['manage_self_user'],
            data={
                'username': 'new' + self.user_test.username
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_user_error(self):
        # Manage user on put by a not loged user should return http401
        response = self.client.put(
            path=self.paths['manage_self_user'],
            data={
                'username': 'new' + self.user_test.username
            }
        )
        self.assertEqual(response.status_code, 401)
        # Manage user on put by a loged user with not valid data should return http400
        self.client.force_login(self.user_test)
        response = self.client.put(
            path=self.paths['manage_self_user'],
            data={
                'username': ''
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_other_method_error(self):
        # Any other HTTP verb should return http405
        http_verbs = [
            self.client.delete,
            self.client.post,
        ]
        self.client.force_login(self.user_test)
        self.check_error_method(http_verbs, self.paths['manage_self_user'])
