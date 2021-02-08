class User:
    def __init__(self, name=""):
        self._name = name

    # getter method
    def get_name(self):
        return self._name

    # setter method
    def set_name(self, x):
        self._name = x
