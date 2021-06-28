class Transaction:

    def __init__(self, transaction_id, amount, is_assigned, employee, assigned_by, assigned_timestamp):
        self._transaction_id = transaction_id
        self.amount = amount
        self._employee = employee
        self._is_assigned = is_assigned
        self._assigned_by = assigned_by
        self._assigned_timestamp = assigned_timestamp

    def get_transaction_id(self):
        return self._transaction_id

    def get_assigned_employee(self):
        return self._employee

    def get_status(self):
        return self._is_assigned

    def get_amount(self):
        return self.amount

    def get_assigned_by(self):
        return self._assigned_by

    def get_assigned_timestamp(self):
        return self._assigned_timestamp

    def set_assigned_employee(self, employee):
        self._employee = employee

    def set_status(self, assigned):
        self._is_assigned = assigned

    def set_assigned_by(self, assigned_by):
        self._assigned_by = assigned_by

    def set_assigned_timestamp(self, timestamp):
        self._assigned_timestamp = timestamp

    def __str__(self):
        return self._transaction_id
