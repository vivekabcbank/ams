class Singleton:
    _instance = None  # Class variable to hold the instance

    def __new__(cls):
        # This method is called when a new instance is created
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.value = 0
        return cls._instance

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self.value

s1 = Singleton()
s2 = Singleton()

print(s1 is s2)

print(s1.get_value())

s1.set_value(32)

print(s1.get_value())
print(s2.get_value())

