import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report
from matplotlib import pyplot as plt

births = pd.read_csv('births.csv')

# (a) Recode child birth variable
births['home'] = ['at_home' if birth == "first line child birth, at home" else 'not_at_home' for birth in births['child_birth']]

# (b) Recode parity variable
births['pari'] = ['primi' if parity == '1' else 'multi' for parity in births['parity']]

# Print unique values for ethnicity
# print(births['etnicity'].unique())
# > ['Dutch' 'Mediterranean' 'Hindu' 'other European' 'Creole' 'Asian' 'other']

# (c) Recode etnicity variable
births['etni'] = ['Dutch' if ethnicity == 'Dutch' else 'Not Dutch' for ethnicity in births['etnicity']]

# (d) Create logistic regression model

X = pd.get_dummies(births[['pari', 'age_cat', 'etni', 'urban']])
Y = births['home']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
model_lr = LogisticRegression(max_iter=1000)
model_lr.fit(X_train, Y_train)
Y_pred = model_lr.predict(X_test)
print(classification_report(Y_test, Y_pred))

# (e) Create decision tree model
model_dt = DecisionTreeClassifier()
model_dt.fit(X_train, Y_train)
plot_tree(model_dt, fontsize=5)

# # (f) Compare models with cross validation

lr_scores = cross_val_score(model_lr, X, Y, cv=5)
dt_scores = cross_val_score(model_dt, X, Y, cv=5)

print("Logistic Regression Cross Validation Scores:")
print(lr_scores)
print(f"Mean: {np.mean(lr_scores)}\n")
print("Decision Tree Cross Validation Scores:")
print(dt_scores)
print(f"Mean: {np.mean(dt_scores)}\n")

# Compare models
print()
if np.mean(lr_scores) > np.mean(dt_scores):
    print("Logistic Regression model fits the data better.")
else:
    print("Decision Tree model fits the data better.")

plt.show()