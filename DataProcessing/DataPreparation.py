import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE


class DataPreparation:

    def scale(data_set):
        scaled_set = pd.DataFrame(data_set)
        robust_scaler = RobustScaler()
        amount_scaled = robust_scaler.fit_transform(scaled_set['Amount'].values.reshape(-1, 1))
        time_scaled = robust_scaler.fit_transform(scaled_set['Time'].values.reshape(-1, 1))
        scaled_set.insert(0, "Amount_Scaled", amount_scaled)
        scaled_set.insert(1, "Time_Scaled", time_scaled)
        scaled_set.drop(['Amount', 'Time'], axis=1, inplace=True)
        return scaled_set

    def splitting_data_set(data_file):
        raw_data = pd.read_csv(data_file)

    # Splitting Data into training and test sets
        no_class = raw_data.drop(['Class'], axis=1)
        class_only = raw_data['Class']

        no_class_train, no_class_test, class_only_train, class_only_test = \
            train_test_split(no_class, class_only, test_size=0.30, random_state=0, stratify=class_only)

    # Adding needed columns to no_class_test
        no_class_test = pd.DataFrame(no_class_test)
        no_class_test['Transaction_Id'] = no_class_test.index + 1
        no_class_test['Processed'] = 0  # add column to determine if row has been processed
        no_class_test['Prediction'] = None

    # Adding Processed Column to class_only_test
        class_only_test = pd.DataFrame(class_only_test, columns=['Class'])
        class_only_test.insert(0, 'Processed', 0, True)

        no_class_test.to_csv('./Resources/DataSets/no_class_not_scaled_test.csv', index=False)
        class_only_test.to_csv('./Resources/DataSets/class_only_test.csv', index=False)

    # All fields in data set except for Time and Amount are scaled. Therefore, Amount and Time should also be scaled.
        no_class_train = DataPreparation.scale(no_class_train)

        # Applying Smote to Training Set
        sm = SMOTE(random_state=2)
        no_class_train, class_only_train = sm.fit_resample(no_class_train, class_only_train.ravel())

        pd.DataFrame(no_class_train).to_csv('./Resources/DataSets/no_class_scaled_train.csv', index=False)
        pd.DataFrame(class_only_train).to_csv('./Resources/DataSets/class_only_train.csv', index=False)
