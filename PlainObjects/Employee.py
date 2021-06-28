class Employee:
    def __init__(self, employee_id, name, num_cases):
        self._id = employee_id
        self._name = name
        self._num_cases = num_cases

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def add_case(self):
        self._num_cases += 1

    def get_num_cases(self):
        return self._num_cases

    def __str__(self):
        return self._name
