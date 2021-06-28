import pandas as pd
from PlainObjects.Employee import Employee


class EmployeesManager:
    def __init__(self):
        self._employee_list = []
        employees_table = pd.read_csv('./Resources/employees.csv')
        for row in employees_table.index:
            e_id = employees_table['Employee_Id'][row]
            name = employees_table['Employee_Name'][row]
            num_cases = employees_table['#_of_Assigned Cases'][row]
            employee = Employee(e_id, name, num_cases)
            self._employee_list.append(employee)

    def get_all_employees(self):
        return self._employee_list

    def get_employee(self, e_id):
        for employee in self._employee_list:
            if employee.get_id() == e_id:
                return employee
        return None
