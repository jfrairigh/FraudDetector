from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_curve
from DataProcessing.DataPreparation import DataPreparation
import time
import pickle
import pandas as pd


class Categorizer:
    def __init__(self):
        self.no_class_not_scaled_test = pd.read_csv('./Resources/DataSets/no_class_not_scaled_test.csv')

        try:
            self.process_stats = pickle.load(open('./Resources/last_process_stats', 'rb'))
        except FileNotFoundError:
            self.process_stats = None

    def train_random_forest(self, model_file_name, estimators=175):
        no_class_train = pd.read_csv('./Resources/DataSets/no_class_scaled_train.csv')
        class_train = pd.read_csv('./Resources/DataSets/class_only_train.csv')
        model = RandomForestClassifier(n_estimators=estimators)
        model.fit(no_class_train, class_train)
        pickle.dump(model, open(model_file_name, 'wb'))  # save model to file

    def predict(self, model_file_name='./Resources/Models/random_forest_150'):
        not_processed_no_class = self.no_class_not_scaled_test[self.no_class_not_scaled_test.Processed == 0]  # collect all new transactions

        # If new transactions exist process them
        if not not_processed_no_class.empty:
            class_test = pd.read_csv('./Resources/DataSets/class_only_test.csv')
            new_class_test = class_test[class_test.Processed == 0]  # collect all new transactions for class only set
            new_class_test = new_class_test['Class']

            # Prep set for random forest algorithm
            no_class_scaled_test = DataPreparation.scale(not_processed_no_class)  # scale Time and Amount

            drop_columns = ['Processed', 'Transaction_Id', 'Prediction']
            for column in drop_columns:
                no_class_scaled_test.drop(column, axis=1, inplace=True)  # drop column

            # Categorizing transactions
            loaded_model = pickle.load(open(model_file_name, 'rb'))  # retrieve model from file
            start = time.time()
            prediction = loaded_model.predict(no_class_scaled_test)
            finished = time.time()
            prediction = pd.DataFrame(prediction, columns=['Prediction'])
            self.no_class_not_scaled_test['Prediction'].fillna(prediction['Prediction'], inplace=True)  # log predictions

            prediction_time = finished - start  # gathering time length for prediction

            # Preparing data for precision recall curve
            y_pred_prob = loaded_model.predict_proba(no_class_scaled_test)[:, 1]
            precision, recall, thresholds = precision_recall_curve(new_class_test, y_pred_prob)
            curve_data = [precision, recall, thresholds]

            # Preparing classification report
            labels = ['Non-Fraud', 'Fraud']
            class_report = classification_report(new_class_test, prediction, target_names=labels, output_dict=True)

            # Saving information for later use
            self.process_stats = {'length': len(not_processed_no_class), 'time': prediction_time,
                                  'curve_data': curve_data, 'classification_report': class_report}
            pickle.dump(self.process_stats, open('./Resources/last_process_stats', 'wb'))

            # Add new fraud transactions to fraud set
            fraud_temp = pd.read_csv('./Resources/CSVLogs/fraud_transactions.csv')
            not_processed_no_class['Prediction'].fillna(prediction['Prediction'], inplace=True)  # add prediction value to new rows
            fraud_df = not_processed_no_class[not_processed_no_class.Prediction == 1]
            fraud_df = fraud_df[['Transaction_Id', 'Amount']]
            fraud_transactions = fraud_temp.append(fraud_df)
            fraud_transactions['Assigned'].fillna(0, inplace=True)
            fraud_transactions.to_csv('./Resources/CSVLogs/fraud_transactions.csv', index=False)

            # Prep main set for next use and save it
            self.no_class_not_scaled_test['Processed'] = self.no_class_not_scaled_test['Processed'].replace([0], 1)  # mark rows as processed
            self.no_class_not_scaled_test.to_csv('./Resources/DataSets/no_class_not_scaled_test.csv', index=False)  # save file

    def get_classification_report(self):
        return self.process_stats['classification_report']

    def get_pr_curve_data(self):
        return self.process_stats['curve_data']

    def get_prediction_time(self):
        return self.process_stats['time']

    def get_batch_length(self):
        return self.process_stats['length']

    def count_positive_predictions(self):  # get count of all transactions predicted to be fraud
        fraud = self.no_class_not_scaled_test[self.no_class_not_scaled_test.Prediction == 1]
        x, y = fraud.shape
        return x

    def count_negative_predictions(self):
        legit = self.no_class_not_scaled_test[self.no_class_not_scaled_test.Prediction == 0]
        x, y = legit.shape
        return x
