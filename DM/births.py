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
X = births[['pari', 'age_cat', 'etni', 'urban']]
X = pd.get_dummies(X, columns=['pari', 'age_cat', 'etni', 'urban'])
Y = births['home']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
print(classification_report(Y_test, Y_pred))

# (e) Create decision tree model
model_dt = DecisionTreeClassifier(max_depth=3, criterion='entropy')
model_dt.fit(X_train, Y_train)
plot_tree(model_dt)
plt.show()

# (f) Compare models with cross validation
scores_logreg = cross_val_score(model, X, Y, cv=10)
scores_dt = cross_val_score(model_dt, X, Y, cv=10)
print("Logistic Regression Accuracy: %0.2f (+/- %0.2f)" % (scores_logreg.mean(), scores_logreg.std() * 2))
print("Decision Tree Accuracy: %0.2f (+/- %0.2f)" % (scores_dt.mean(), scores_dt.std() * 2))