from rest_framework.test import APITestCase


class TestCategoryAPI(APITestCase):
    def test_list_category(self):
        response = self.client.get("/api/categories/")
        expected_data = [
            {"id": 1, "name": "Category 1"},
            {"id": 2, "name": "Category 2"},
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
