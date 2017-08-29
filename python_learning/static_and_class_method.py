

class Methods(object):
    print("invoke Class")

    def __init__(self, data):
        self.data = data

    # public method
    def self_method(self):
        print("self method: " + self.data)

    @classmethod
    def class_method(cls, data):
        cls.static_method(data)
        print("Class Method: " + data)

    @staticmethod
    def static_method(data):
        print("Static Method: "  + data)

    # protected method
    def _single_underscore(self):
        print("single underscore: " + self.data)

    # private method
    def __double_underscore(self):
        print("double underscore: " + self.data)

data = "method"
method = Methods(data)

method.self_method()
method.class_method(data)
method.static_method(data)
method._single_underscore()
# method.__double_underscore()   # 方法不能调用,因为是private

Methods.class_method(data)
Methods.static_method(data)
