from uuid import UUID
import pytest

from src.core.category.application.create_category import (
    InvalidCategoryData,
    create_category,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        category_id = create_category(
            name="name", description="description", is_active=True
        )

        assert category_id is not None
        assert isinstance(category_id, UUID)

    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategoryData, match="Name is required") as exc_info:
            create_category(name="")
        assert exc_info.type == InvalidCategoryData
