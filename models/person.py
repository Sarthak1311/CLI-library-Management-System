from abc import ABC, abstractmethod
class Person(ABC):
    def __init__ (self,id,name,email):
        self.id =id
        self.name = name 
        self.email = email

    @abstractmethod
    def display_role(self):
        """Every type of person should define there role """
        pass
    
