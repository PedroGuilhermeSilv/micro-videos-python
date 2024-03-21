import json
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateEditCategory:
    def test_user_can_create_and_edit_category(self):
        api_client = APIClient()

        # list categories
        list_categories = api_client.get("/api/categories/")
        assert list_categories.status_code == 200
        assert list_categories.data == {"data": []}

        # create category
        create_response = api_client.post(
            "/api/categories/",
            {"name": "Category 1", "description": "Description 1", "is_active": True},
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        # list category
        list_categories = api_client.get("/api/categories/")
        assert list_categories.status_code == 200
        assert list_categories.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Category 1",
                    "description": "Description 1",
                    "is_active": True,
                }
            ]
        }

        # retrieve category
        category = api_client.get(f"/api/categories/{created_category_id}/")
        assert category.status_code == 200
        assert category.data["data"] == {
            "id": created_category_id,
            "name": "Category 1",
            "description": "Description 1",
            "is_active": True,
        }

        # edit category
        api_client.put(
            f"/api/categories/{created_category_id}/",
            content_type="application/json",
            data=json.dumps(
                {
                    "name": "Category 2",
                    "description": "Description 2",
                    "is_active": False,
                }
            ),
        )

        # retrieve category
        category = api_client.get(f"/api/categories/{created_category_id}/")
        assert category.status_code == 200
        assert category.data["data"] == {
            "id": created_category_id,
            "name": "Category 2",
            "description": "Description 2",
            "is_active": False,
        }
