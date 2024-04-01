from dataclasses import dataclass, field
import uuid
from uuid import UUID


@dataclass
class Genre:
    name: str
    is_active: bool = True
    id: UUID = field(default_factory=uuid.uuid4)
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("Name must have less than 255 characters")
        if not self.name:
            raise ValueError("Name is required")

    def __str__(self) -> str:
        return (
            f"Genre: {self.name} - {self.is_active} - {self.id} - {self.categories}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Initially this class only checks if the instances are at the same memory address.
        We need to compare the id."""
        if not isinstance(other, Genre):
            raise ValueError("Comparison between different classes")
        if self.id == other.id:
            return True

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
