from django.test import TestCase
from django.utils import timezone

from dj_vpn.accounts.models import User


class PointTest(TestCase):
    def setUp(self):
        point_user = User.objects.create_user(username='test_user', email='test@gmail.com', password='<PASSWORD>',
                                              first_name='test',
                                              last_name='tests')
        self.test_user = point_user

    def test_normal_user(self):
        self.assertEqual(self.test_user.account_type, 'normal_user')

    def test_accounts_is_active(self):
        """
        account is active and user not deleted
        """
        self.assertTrue(self.test_user.is_active)

    def test_accounts_is_not_deleted(self):
        self.assertEqual(self.test_user.is_deleted, None)
        self.assertEqual(self.test_user.deleted_at, None)

    def test_accounts_status(self):
        self.assertEqual(self.test_user.accounts_status, 'limit')

    def test_get_user_information(self):
        self.assertEqual(self.test_user.first_name, "test")
        self.assertEqual(self.test_user.last_name, "tests")
        self.assertEqual(self.test_user.email, "test@gmail.com")
        self.assertEqual(self.test_user.username, "test_user")
        self.assertEqual(self.test_user.start_premium, timezone.localdate())
        self.assertEqual(self.test_user.number_of_max_device, 1)
        self.assertEqual(self.test_user.last_login, None)
        self.assertEqual(self.test_user.volume, 0)
        self.assertEqual(self.test_user.volume_usage, 0)
        self.assertFalse(self.test_user.is_connected_user)