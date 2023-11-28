from .base_authentication import BaseAuthenticationTest


class TestUpdatePassword(BaseAuthenticationTest):
    paths_name = {
        'update_password': 'authentication:update-password'
    }

    def test_update_success(self):
        # update password with valid data should return http200
        self.client.force_login(self.user_test)
        response = self.client.post(
            path=self.paths['update_password'],
            data={
                'old_password': self.user_data['password'],
                'new_password': self.user_data['password'] + '56new'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.user_test.refresh_from_db()
        self.assertTrue(self.user_test.check_password(self.user_data['password'] + '56new'))

    def test_update_error(self):
        # update password without get loged should return http401
        response = self.client.post(
            path=self.paths['update_password'],
            data={
                'old_password': self.user_data['password'],
                'new_password': self.user_data['password'] + '56new'
            }
        )
        self.assertEqual(response.status_code, 401)
        # update password with wrong old password should return http403
        self.client.force_login(self.user_test)
        response = self.client.post(
            path=self.paths['update_password'],
            data={
                'old_password': self.user_data['password'] + 'wrong',
                'new_password': self.user_data['password'] + '56new'
            }
        )
        self.assertEqual(response.status_code, 403)
        # update password with not valid new password should return http400
        response = self.client.post(
            path=self.paths['update_password'],
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
        self.client.force_login(self.user_test)
        self.check_error_method(http_verbs, self.paths['update_password'])
