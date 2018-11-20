import os
import unittest


from flask_testing import TestCase
from project import create_app


app = create_app()


class TestDevelopmentConfig(TestCase):
    """Test Development Config"""

    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_config(self):
        """Ensure Development config is right"""
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(app.config['DEBUG'])
        self.assertEqual(
            app.config['SECRET_KEY'],
            os.environ.get('SECRET_KEY'))
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'],
            os.environ.get('DATABASE_URL'))
        self.assertTrue(app.config['SQLALCHEMY_ECHO'])
        self.assertFalse(app.config['USERS_SERVICE_MOCK'])


class TestTestingConfig(TestCase):
    """Test Testing Config"""

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_config(self):
        """Ensure Testing config is right"""
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(app.config['DEBUG'])
        self.assertEqual(
            app.config['SECRET_KEY'],
            os.environ.get('SECRET_KEY'))
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'],
            os.environ.get('DATABASE_TEST_URL'))
        self.assertFalse(app.config['SQLALCHEMY_ECHO'])
        self.assertTrue(app.config['USERS_SERVICE_MOCK'])


class TestStagingConfig(TestCase):
    """Test Staging Config"""

    def create_app(self):
        app.config.from_object('project.config.StagingConfig')
        return app

    def test_config(self):
        """Ensure Staging config is right"""
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(app.config['DEBUG'])
        self.assertEqual(
            app.config['SECRET_KEY'],
            os.environ.get('SECRET_KEY'))
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'],
            os.environ.get('DATABASE_URL'))
        self.assertFalse(app.config['SQLALCHEMY_ECHO'])
        self.assertFalse(app.config['USERS_SERVICE_MOCK'])


class TestProductionConfig(TestCase):
    """Test Production Config"""

    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_config(self):
        """Ensure Production config is right"""
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG'])
        self.assertEqual(
            app.config['SECRET_KEY'],
            os.environ.get('SECRET_KEY'))
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertEqual(
            app.config['SQLALCHEMY_DATABASE_URI'],
            os.environ.get('DATABASE_URL'))
        self.assertFalse(app.config['SQLALCHEMY_ECHO'])
        self.assertFalse(app.config['USERS_SERVICE_MOCK'])


if __name__ == '__main__':
    unittest.main()
