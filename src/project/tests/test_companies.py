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
            self.assertEqual(response.status_code, 403)


class TestCreateCompany(BaseTestCase):
    """Test Create Company"""

    def test_admin_users_can_create_companies(self):
        """Test admin users can create companies"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        data = {
            'identifier': random_string(),
            'name': random_string()
        }

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.post(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            response_data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertEqual(Company.query.count(), 1)
            self.assertEqual(response_data['identifier'], data['identifier'])
            self.assertEqual(response_data['name'], data['name'])
            self.assertEqual(Company.query.first().created_by, admin['id'])

    def test_not_admin_users_cant_create_companies(self):
        """Test not admin users can't create companies"""
        auth = AuthenticatorFactory.get_instance().clear()
        user = add_user(admin=False)
        auth.set_user(user)

        data = {
            'identifier': random_string(),
            'name': random_string()
        }

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.post(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 403)
            self.assertEqual(Company.query.count(), 0)

    def test_create_a_company_without_identifier(self):
        """Test creating a company without identifier"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        data = {
            'identifier': random_string()
        }

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.post(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 0)

    def test_create_a_company_without_name(self):
        """Test creating a company without name"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        data = {
            'name': random_string()
        }

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.post(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 0)

    def test_create_a_company_with_empty_data(self):
        """Test creating a company without name"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        data = {}

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.post(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 0)

    def test_create_a_company_without_data(self):
        """Test creating a company without name"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.post(
                '/companies',
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 0)


class TestUpdateCompany(BaseTestCase):
    """Test Update Company"""

    def test_admin_users_can_update_companies(self):
        """Test admin users can update companies"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()

        data = {
            'identifier': random_string(),
            'name': random_string()
        }

        self.assertEqual(Company.query.count(), 1)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            response_data = json.loads(response.data.decode())

            updated_company = Company.query.first()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(Company.query.count(), 1)
            self.assertEqual(response_data['identifier'], data['identifier'])
            self.assertEqual(response_data['name'], data['name'])
            self.assertIsNotNone(updated_company.updated)
            self.assertEqual(updated_company.updated_by, admin['id'])

    def test_not_admin_users_cant_update_companies(self):
        """Test not admin users can't update companies"""
        auth = AuthenticatorFactory.get_instance().clear()
        user = add_user(admin=False)
        auth.set_user(user)

        data = {
            'identifier': random_string(),
            'name': random_string()
        }

        company = add_company()

        self.assertEqual(Company.query.count(), 1)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            company = Company.query.filter_by(id=company.id).first()

            self.assertEqual(response.status_code, 403)
            self.assertEqual(Company.query.count(), 1)
            self.assertNotEqual(company.identifier, data['identifier'])
            self.assertNotEqual(company.name, data['name'])

    def test_update_a_company_without_identifier(self):
        """Test update a company without identifier"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()

        data = {
            'name': random_string()
        }

        self.assertEqual(Company.query.count(), 1)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            company = Company.query.filter_by(id=company.id).first()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 1)
            self.assertIsNotNone(company.identifier)
            self.assertNotEqual(company.name, data['name'])

    def test_update_a_company_without_name(self):
        """Test update a company without name"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()

        data = {
            'identifier': random_string()
        }

        self.assertEqual(Company.query.count(), 1)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            company = Company.query.filter_by(id=company.id).first()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 1)
            self.assertIsNotNone(company.name)
            self.assertNotEqual(company.identifier, data['identifier'])

    def test_update_a_company_with_empty_data(self):
        """Test update a company with empty data"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()

        data = {}

        self.assertEqual(Company.query.count(), 1)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            company = Company.query.filter_by(id=company.id).first()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 1)
            self.assertIsNotNone(company.name)
            self.assertIsNotNone(company.identifier)

    def test_update_a_company_without_data(self):
        """Test update a company without data"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()

        self.assertEqual(Company.query.count(), 1)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            company = Company.query.filter_by(id=company.id).first()

            self.assertEqual(response.status_code, 400)
            self.assertEqual(Company.query.count(), 1)
            self.assertIsNotNone(company.name)
            self.assertIsNotNone(company.identifier)

    def test_update_a_non_existing_company(self):
        """Test update a non existing company"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        data = {
            'identifier': random_string(),
            'name': random_string()
        }

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.put(
                '/companies/{}'.format(random.randint(10, 100)),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                data=json.dumps(data),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(Company.query.count(), 0)


class TestDeleteCompany(BaseTestCase):
    """Deleting Company Tests"""

    def test_admin_can_delete_a_company(self):
        """An admin user can delete a company"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()

        self.assertEqual(Company.query.count(), 1)
        self.assertTrue(Company.query.first().active)

        with self.client:
            response = self.client.delete(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            company = Company.query.first()

            self.assertEqual(response.status_code, 204)
            self.assertEqual(Company.query.count(), 1)
            self.assertFalse(company.active)
            self.assertEqual(company.updated_by, admin['id'])

    def test_no_admin_user_cant_delete_a_company(self):
        """A not admin user can't delete a company"""
        auth = AuthenticatorFactory.get_instance().clear()
        user = add_user(admin=False)
        auth.set_user(user)

        company = add_company()

        self.assertEqual(Company.query.count(), 1)
        self.assertTrue(Company.query.first().active)

        with self.client:
            response = self.client.delete(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 403)
            self.assertEqual(Company.query.count(), 1)
            self.assertTrue(Company.query.first().active)
            self.assertIsNone(company.updated_by)

    def test_delete_a_no_existing_company(self):
        """Delete a no existing company"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        self.assertEqual(Company.query.count(), 0)

        with self.client:
            response = self.client.delete(
                '/companies/{}'.format(random.randint(10, 100)),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 404)

    def test_delete_an_already_deleted_company(self):
        """Delete an already deleted company"""
        auth = AuthenticatorFactory.get_instance().clear()
        admin = add_user(admin=True)
        auth.set_user(admin)

        company = add_company()
        company.active = False

        db.session.add(company)
        db.session.commit()

        self.assertEqual(Company.query.count(), 1)
        self.assertFalse(Company.query.first().active)

        with self.client:
            response = self.client.delete(
                '/companies/{}'.format(company.id),
                headers={'Authorization': 'Bearer {}'.format(random_string())},
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 404)
            self.assertFalse(Company.query.first().active)


if __name__ == '__main__':
    unittest.main()
