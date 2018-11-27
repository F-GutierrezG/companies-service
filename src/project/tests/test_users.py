import json
import random
import unittest

from project.tests.utils import random_string

from project import db
from project.models import Company, UserCompanies
from project.services import UsersServiceFactory
from project.auth import AuthenticatorFactory

from project.tests.base import BaseTestCase


class TestListUsers(BaseTestCase):
    """Tests for list users"""

    def _add_company(self):
        company = Company(name=random_string())

        db.session.add(company)
        db.session.commit()

        return company

    def _add_user(self, admin=False):
        users_service = UsersServiceFactory.get_instance()
        user = {
            'id': random.randint(0, 100000),
            'first_name': random_string(),
            'last_name': random_string(),
            'email': '{}@test.com'.format(random_string),
            'admin': admin
        }
        users_service.add_user(user)
        return user

    def _add_user_to_company(self, user, company):
        user_company = UserCompanies(user_id=user['id'], company_id=company.id)

        db.session.add(user_company)
        db.session.commit()

        return user_company

    def test_list_users_if_admin(self):
        """List users if are requested by an admin"""
        users_service = UsersServiceFactory.get_instance()
        users_service.clear()
        authenticator = AuthenticatorFactory.get_instance()

        admin = self._add_user(admin=True)

        admins_quantity = random.randint(4, 10)

        for i in range(0, admins_quantity):
            self._add_user(admin=True)

        authenticator.set_user(admin)

        response = self.client.get(
            '/companies/users',
            headers={'Authorization': 'Bearer {}'.format(random_string())},
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), admins_quantity + 1)

    def test_list_users_in_a_company_if_admin(self):
        """List users on a specific company by an admin"""
        users_service = UsersServiceFactory.get_instance()
        users_service.clear()
        authenticator = AuthenticatorFactory.get_instance()

        admin = self._add_user(admin=True)
        authenticator.set_user(admin)

        company = self._add_company()

        users_quantity = random.randint(4, 10)

        for i in range(0, users_quantity):
            user = self._add_user(admin=False)
            self._add_user_to_company(user, company)

        response = self.client.get(
            '/companies/{}/users'.format(company.id),
            headers={'Authorization': 'Bearer {}'.format(random_string())},
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), users_quantity)

    def test_list_users_in_same_company(self):
        """List users on the same company by a company user"""
        users_service = UsersServiceFactory.get_instance()
        users_service.clear()
        authenticator = AuthenticatorFactory.get_instance()

        current_user = self._add_user()
        authenticator.set_user(current_user)

        company = self._add_company()

        self._add_user_to_company(current_user, company)

        users_quantity = random.randint(4, 10)

        for i in range(0, users_quantity):
            user = self._add_user(admin=False)
            self._add_user_to_company(user, company)

        response = self.client.get(
            '/companies/users',
            headers={'Authorization': 'Bearer {}'.format(random_string())},
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), users_quantity + 1)

    def test_list_users_with_no_company(self):
        """List users without company"""
        users_service = UsersServiceFactory.get_instance()
        users_service.clear()
        authenticator = AuthenticatorFactory.get_instance()

        current_user = self._add_user()
        authenticator.set_user(current_user)

        company = self._add_company()

        users_quantity = random.randint(4, 10)

        for i in range(0, users_quantity):
            user = self._add_user(admin=False)
            self._add_user_to_company(user, company)

        response = self.client.get(
            '/companies/users',
            headers={'Authorization': 'Bearer {}'.format(random_string())},
            content_type='application/json'
        )
        response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 0)


if __name__ == '__main__':
    unittest.main()
