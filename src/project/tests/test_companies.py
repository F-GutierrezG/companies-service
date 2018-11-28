import json
import random
import unittest
from auth.factories import AuthenticatorFactory

from project.tests.utils import (
    random_string, add_user, add_company, add_user_to_company)

from project import db
from project.tests.base import BaseTestCase
from project.models import Company, UserCompanies


class BaseCompanyTestCase(BaseTestCase):
    def _add_company(self, users):
        company = Company(
            identifier=random_string(),
            name=random_string())
        for user in users:
            company.users.append(UserCompanies(user_id=user))
        db.session.add(company)
        db.session.commit()
        return company


class TestListCompanies(BaseCompanyTestCase):
    """List user companies"""

    def __get_companies(self, user_id):
        token = 'FAKE_TOKEN'
        with self.client:
            response = self.client.get(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(token)},
                content_type='application/json'
            )
            return response

    def __set_session_user(self, user_id):
        AuthenticatorFactory.get_instance().set_user({
            'id': user_id,
            'first_name': random_string(16),
            'last_name': random_string(16),
            'email': '{}@test.com'.format(random_string(16))
        })

    def test_user_companies(self):
        """List only returns user companies"""
        self._add_company(users=[1, 2])
        self._add_company(users=[2, 3])

        self.assertEqual(len(Company.query.all()), 2)
        self.assertEqual(len(UserCompanies.query.all()), 4)

        self.__set_session_user(user_id=1)
        response = self.__get_companies(user_id=1)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)

        self.__set_session_user(user_id=2)
        response = self.__get_companies(user_id=2)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

        self.__set_session_user(user_id=3)
        response = self.__get_companies(user_id=3)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)


class TestViewCompany(BaseTestCase):
    """View company"""

    def test_view_company_if_admin(self):
        """View a company as admin user"""
        company = add_company()

        admin = add_user(admin=True)
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(admin)

        with self.client:
            response = self.client.get(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())

            self.assertEqual(Company.query.count(), 1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['name'], company.name)

    def test_view_unexisting_company_if_admin(self):
        """View a company as admin user"""
        admin = add_user(admin=True)
        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(admin)

        with self.client:
            response = self.client.get(
                '/companies/{}'.format(random.randint(1, 100)),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            self.assertEqual(Company.query.count(), 0)
            self.assertEqual(response.status_code, 404)

    def test_view_company_if_user_belongs(self):
        """View a company as a company user"""
        company = add_company()
        user = add_user()
        add_user_to_company(user, company)

        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(user)

        with self.client:
            response = self.client.get(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())

            self.assertEqual(Company.query.count(), 1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['name'], company.name)

    def test_view_company_if_user_not_belongs(self):
        """View a company as a not company user"""
        company = add_company()
        user = add_user()

        auth = AuthenticatorFactory.get_instance().clear()
        auth.set_user(user)

        with self.client:
            response = self.client.get(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            self.assertEqual(Company.query.count(), 1)
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
