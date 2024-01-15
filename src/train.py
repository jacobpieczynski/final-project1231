import numpy as np
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sklearn import datasets
import matplotlib.pyplot as plt
from LogisticRegression import LogisticRegression
import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv('log_data.csv')
X = data.drop('Home Win', axis=1)
y = data['Home Win']
#bc = datasets.load_breast_cancer()
#X, y = bc.data, bc.target
#for data in X:
#    print(data, end="\n\n")
model_average, model_best = 0, 0
rng = 100
for i in range(rng):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1) #random_state=705

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    #print(X_train_scaled)
    #model = LogisticRegression()
    #model.fit(X_train_scaled,y_train)
    model = LogisticRegression(lr=0.0001, n_iters=2500)
    model.fit(X_train_scaled,y_train)
    #clf.fit(X_train,y_train)
    #y_pred = clf.predict(X_test)
    y_pred = model.predict(X_test_scaled)

    def accuracy(y_pred, y_test):
        return np.sum(y_pred==y_test)/len(y_test)


    new_game = pd.read_csv('new_game.csv')
    new_data = new_game.drop('Home Win', axis=1)
    new_data_scaled = scaler.transform(new_data)
    prediction = model.predict(new_data_scaled)

    # Display the prediction
    print("Predicted Outcome:", prediction)

    acc = accuracy(y_pred, y_test)
    model_average += acc
    if acc >= model_best:
        model_best = acc
    print(acc)

model_average /= rng

print(f"Overall accuracy is: {model_average}")