import uuid


class Category:
    def __init__(self, name, id="", description="", is_active=True):
        self.name = name
        self.id = id or uuid.uuid4()
        self.description = description
        self.is_active = is_active
    

        if len(name) > 255:
            raise ValueError("Name must have less than 255 characters")

    def __str__(self) -> str:
        return (
            f"Category: {self.name} - {self.id} - {self.description} - {self.is_active}"
        )

    def __repr__(self):
        return self.__str__()
    
    def update_category(self, name: str, description: str):
        self.name = name
        self.description = description