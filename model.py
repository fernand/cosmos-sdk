import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix

X = np.loadtxt('features.csv', delimiter=',')
y = np.loadtxt('labels.csv', delimiter=',')

y_binary = np.zeros(len(y), dtype='int')
for i, pct in enumerate(y):
    if pct >= 34.4:
        y_binary[i] = 1

# X_filtered, y_filtered = [], []
# for features, label in zip(X,y):
#     if label <= 33.6 or label >= 34.5:
#         X_filtered.append(features)
#         if label <= 33.6:
#             y_filtered.append(0)
#         else:
#             y_filtered.append(1)
# X = np.array(X_filtered)
# y_binary = np.array(y_filtered, dtype='int')

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# rf = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=42)
# rf.fit(X_train, y_train)
# print('r2 training score', rf.score(X_train, y_train))
# print('r2 test score', rf.score(X_test, y_test))

X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)
rf = RandomForestClassifier(n_estimators=500, n_jobs=-1, random_state=42)
rf.fit(X_train, y_train)
print('test roc auc score', roc_auc_score(y_test, rf.predict(X_test)))
print('confusion matrix', confusion_matrix(y_test, rf.predict(X_test)))