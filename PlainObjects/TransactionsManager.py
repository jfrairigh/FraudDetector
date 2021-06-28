import pandas as pd
from PlainObjects.Transaction import Transaction


class TransactionsManager:
    def __init__(self, employee_manager):
        self._unassigned_list = []
        self._assigned_list = []
        self._e_manager = employee_manager

        self.fraud = pd.read_csv('./Resources/CSVLogs/fraud_transactions.csv')

        for row in self.fraud.index:  # create transaction objects
            t_id = str(self.fraud['Transaction_Id'][row])
            amount = self.fraud['Amount'][row]
            e_id = self.fraud['Assigned_To'][row]
            employee = self._e_manager.get_employee(e_id)
            assigned = self.fraud['Assigned'][row]
            assigned_by = self.fraud['Assigned_By'][row]
            assigned_timestamp = self.fraud['Date_Time'][row]
            transaction = Transaction(t_id, amount, assigned, employee, assigned_by, assigned_timestamp)
            if assigned == 1:
                employee.add_case()
                self._assigned_list.append(transaction)
            else:
                self._unassigned_list.append(transaction)

    def get_all_unassigned_transactions(self):
        return self._unassigned_list

    def get_all_assigned_transactions(self):
        return self._assigned_list

    def get_unassigned_transaction(self, t_id):
        for trans in self._unassigned_list:
            if trans.get_transaction_id() == t_id:
                return trans
        return None

    def get_unassigned_length(self):
        return len(self._unassigned_list)

    def get_assigned_length(self):
        return len(self._assigned_list)

    def assign(self, t_id, employee, assigned_by, time_stamp):
        trans = self.get_unassigned_transaction(t_id)
        trans.set_status(1)  # set assigned status to true
        trans.set_assigned_employee(employee)
        trans.set_assigned_by(assigned_by)
        trans.set_assigned_timestamp(time_stamp)
        employee.add_case()
        self._unassigned_list.remove(trans)
        self._assigned_list.append(trans)

    def save(self):
        for item in self._assigned_list:
            self.fraud['Transaction_Id'] = self.fraud['Transaction_Id'].apply(str)
            index = self.fraud.index[self.fraud['Transaction_Id'] == item.get_transaction_id()]
            self.fraud.loc[index, ['Assigned', 'Assigned_By', 'Assigned_To', 'Date_Time']] = \
                [item.get_status(), item.get_assigned_by(), item.get_assigned_employee().get_id(),
                 item.get_assigned_timestamp()]  # update values of assigned transactions

        self.fraud.to_csv('./Resources/CSVLogs/fraud_transactions.csv', index=False)
