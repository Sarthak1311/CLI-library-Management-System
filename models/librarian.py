from .person import Person

class Librarian(Person):
    def __init__(self, id, name, email,employee_id):
        super().__init__(id, name, email)
        self.employee_id = employee_id

    def display_role(self):
        print(f"{self.name} is a librarian")
        return super().display_role()

    