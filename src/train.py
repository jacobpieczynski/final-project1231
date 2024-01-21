import numpy as np
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor # TEMP - FOR VAR IMPORTANCE
from sklearn.metrics import accuracy_score # TMP FOR VAR IMPORTANCE
from sklearn.preprocessing import StandardScaler

from LogisticRegression import LogisticRegression
import pandas as pd
from scipy import stats

# Load the CSV file into a DataFrame
data = pd.read_csv('log_data.csv').drop(columns=['Gameid', 'Home', 'Visitor', 'Date'], axis=1)
data = pd.get_dummies(data)
#data = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)] # Removing outliers by 3 standard deviations (doesn't seem to do anything)
X = data.drop('Home Win', axis=1)
y = data['Home Win']

# Describes the data - FOR VAR IMPORTANCE
print(data.describe())
feature_list = list(data.columns)
print(feature_list)
#bc = datasets.load_breast_cancer()
#X, y = bc.data, bc.target
#for data in X:
#    print(data, end="\n\n")
model_average, model_best, rf_model_average = 0, 0, 0
rng = 10
for i in range(rng):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1) #random_state=705

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    #model = LogisticRegression()
    rf_model = RandomForestRegressor(n_estimators = 1000, random_state = 42) # DELETE AFTER VAR IMPORTANCE
    rf_model.fit(X_train_scaled, y_train)
    rf_y_pred = rf_model.predict(X_test_scaled)
    model = LogisticRegression(lr=0.0001, n_iters=2500)
    model.fit(X_train_scaled,y_train)
    y_pred = model.predict(X_test_scaled)

    def accuracy(y_pred, y_test):
        return np.sum(y_pred==y_test)/len(y_test)

    # JUST TO GET VARIABLE IMPORTANCE - DELETE
    # Get numerical feature importances
    importances = list(rf_model.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature and importances 
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]
    rf_y_pred = np.where(rf_y_pred >= 0.5, 1, 0)
    rf_acc = accuracy_score(y_test, rf_y_pred)
    print('RF Accuracy:', rf_acc, '%.')

    """
    new_game = pd.read_csv('new_game.csv')
    new_data = new_game.drop('Home Win', axis=1)
    new_data_scaled = scaler.transform(new_data)
    prediction = model.predict(new_data_scaled)

    # Display the prediction
    print("Predicted Outcome:", prediction)
    """
    
    acc = accuracy(y_pred, y_test)
    model_average += acc
    rf_model_average += rf_acc
    if acc >= model_best:
        model_best = acc
    print(f"LR Accuracy: {acc}")

model_average /= rng
rf_model_average /= rng

print(f"Best accuracy is {model_best}")
print(f"Overall accuracy Random Forest is: {rf_model_average}")
print(f"Overall accuracy Linear Regression is: {model_average}")