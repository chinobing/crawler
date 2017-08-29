
class Supper(object):
    """
    Supper class, Contains some methods to be inherited.
    """
    def __init__(self):
        self.name = None
        self.age = None

    def get_age(self):
        return self.age

    def get_name(self):
        return self.name

    def print_age(self):
        print(self.age)

    def print_name(self):
        print(self.name)

    def show(self):
        print('hello world')


class Student(Supper):
    """
    Inherit print method but assign field new value
    """
    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age

    def show(self):
        super().show()
        self.print_age()
        self.print_name()


if __name__ == "__main__":
    s = Student("123", 123)
    s.show()

