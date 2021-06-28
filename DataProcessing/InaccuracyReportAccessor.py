import pandas as pd


class InaccuracyReportAccessor:
    def __init__(self):
        self.inaccuracy_reported = pd.read_csv("./Resources/CSVLogs/inaccuracy_report.csv")
        self.inaccuracy_reported['Transaction_Id'] = self.inaccuracy_reported['Transaction_Id'].astype(str)

    def report_new(self, transaction_id, category):
        matches = self.inaccuracy_reported.loc[self.inaccuracy_reported['Transaction_Id'].str.contains(transaction_id)]
        if matches.empty:  # if prediction error hasn't already been reported
            new_row = {'Transaction_Id': str(transaction_id), 'Category': category}
            update_log = self.inaccuracy_reported.append(new_row, ignore_index=True)
            self.inaccuracy_reported = pd.DataFrame(update_log)
            self.inaccuracy_reported.to_csv("./Resources/CSVLogs/inaccuracy_report.csv", index=False)
            return True
        else:
            return False

    def count_category(self, category):
        fp = self.inaccuracy_reported.loc[self.inaccuracy_reported['Category'].str.contains(category)]
        x, y = fp.shape
        return x
