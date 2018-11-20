import json
import unittest

from project.tests.utils import random_string

from project import db
from project.tests.base import BaseTestCase
from project.models import Company


class TestListCompanies(BaseTestCase):
    """List user companies"""

    def test_user_companies(self):
        with self.client:
            response = self.client.get(
                '/companies',
                # headers={'Authorization': 'Bearer {}'.format(token)},
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response_data),
                Company.query.count())


class TestViewCompany(BaseTestCase):
    """View user companies"""
    pass


if __name__ == '__main__':
    unittest.main()
