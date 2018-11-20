import json
import unittest

from project.tests.utils import random_string

from project import db
from project.tests.base import BaseTestCase
from project.models import Company, UserCompanies
from project.auth import AuthenticatorFactory


class TestListCompanies(BaseTestCase):
    """List user companies"""

    def __add_company(self, users):
        company = Company(name=random_string(16))
        for user in users:
            company.users.append(UserCompanies(user_id=user))
        db.session.add(company)
        db.session.commit()
        return company

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
        self.__add_company(users=[1, 2])
        self.__add_company(users=[2, 3])

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
    """View user companies"""
    pass


if __name__ == '__main__':
    unittest.main()
