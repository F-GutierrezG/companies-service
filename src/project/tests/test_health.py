import json
import unittest
from project.tests.base import BaseTestCase


class TestUserServiceHealth(BaseTestCase):
    """Tests for health of CompaniesService"""

    def test_health(self):
        """Ensure health route behaves correctly."""
        response = self.client.get('/companies-service/health')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('healthy', data['message'])


if __name__ == '__main__':
    unittest.main()
