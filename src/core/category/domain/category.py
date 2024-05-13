from dataclasses import dataclass, field
import uuid
from uuid import UUID


@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("Name must have less than 255 characters")
        if not self.name:
            raise ValueError("Name is required")

    def __str__(self) -> str:
        return (
            f"Category: {self.name} - {self.id} - {self.description} - {self.is_active}"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Initially this class only checks if the instances are at the same memory address.
        We need to compare the id."""
        if not isinstance(other, Category):
            raise ValueError("Comparison between different classes")
        if self.id == other.id:
            return True

    def update_category(self, name: str, description: str):
        self.name = name
        self.description = description
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()
